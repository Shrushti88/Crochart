import React, { useState, useEffect, useCallback, useRef } from 'react';
import {
  CrochetPatternAST,
  ValidationReport,
  ChartGraph,
  ChartNode,
  TerminologyStandard,
  SamplePattern,
  DBProject
} from './types';
import { ApiService } from './services/api';
import { ChartCanvas } from './components/Canvas/ChartCanvas';
import { PlaybackControls } from './components/Canvas/PlaybackControls';
import { PatternEditor } from './components/Editor/PatternEditor';
import { ValidationPanel } from './components/Diagnostics/ValidationPanel';
import { SampleGallery } from './components/Gallery/SampleGallery';
import { ProjectsModal } from './components/Projects/ProjectsModal';
import { ExportModal } from './components/Export/ExportModal';
import { MLStudioModal } from './components/MLStudio/MLStudioModal';
import {
  Sparkles,
  BookOpen,
  FolderArchive,
  Download,
  BrainCircuit,
  Sun,
  Moon,
  AlertTriangle,
  Edit3
} from 'lucide-react';

const DEFAULT_PATTERN = `Round 1: Magic ring, 6 sc (6)
Round 2: [inc] * 6 (12)
Round 3: [inc, sc] * 6 (18)
Round 4: [inc, 2 sc] * 6 (24)
Round 5: [inc, 3 sc] * 6 (30)
Round 6: [inc, 4 sc] * 6 (36)
Round 7: [inc, 5 sc] * 6 (42)
Round 8: [inc, 6 sc] * 6 (48)
Round 9: [inc, 7 sc] * 6 (54)
Round 10: [inc, 8 sc] * 6 (60)`;

export const App: React.FC = () => {
  // Pattern state
  const [patternTitle, setPatternTitle] = useState<string>('Traditional Crochet Circle with Stacked Increases');
  const [patternText, setPatternText] = useState<string>(DEFAULT_PATTERN);
  const [terminology, setTerminology] = useState<TerminologyStandard>('US');

  // Parsed / Layout State
  const [ast, setAst] = useState<CrochetPatternAST | null>(null);
  const [validation, setValidation] = useState<ValidationReport | null>(null);
  const [chart, setChart] = useState<ChartGraph | null>(null);
  const [selectedNode, setSelectedNode] = useState<ChartNode | null>(null);

  // UI state
  const [isParsing, setIsParsing] = useState<boolean>(false);
  const [sidebarTab, setSidebarTab] = useState<'editor' | 'diagnostics'>('editor');
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');

  // Animation Playback State
  const [currentStep, setCurrentStep] = useState<number>(-1);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);

  // Modals state
  const [galleryOpen, setGalleryOpen] = useState<boolean>(false);
  const [projectsOpen, setProjectsOpen] = useState<boolean>(false);
  const [exportOpen, setExportOpen] = useState<boolean>(false);
  const [mlStudioOpen, setMlStudioOpen] = useState<boolean>(false);
  const [samples, setSamples] = useState<SamplePattern[]>([]);

  const debounceTimerRef = useRef<number | null>(null);

  // Load sample gallery presets
  useEffect(() => {
    ApiService.getSamples()
      .then(data => setSamples(data || []))
      .catch(err => console.error('Failed to load sample library:', err));
  }, []);

  // Live Auto-Parse & Chart Generator
  const runParseAndLayout = useCallback(
    async (text: string, title: string, term: TerminologyStandard) => {
      if (!text || !text.trim()) {
        setAst(null);
        setValidation(null);
        setChart(null);
        return;
      }

      try {
        setIsParsing(true);
        // 1. Parse text & validate
        const parseRes = await ApiService.parseText(text, title, term);
        setAst(parseRes.ast);
        setValidation(parseRes.validation);

        // 2. Generate vector layout graph
        const chartRes = await ApiService.generateChart(parseRes.ast, text, term);
        setChart(chartRes);
      } catch (err: any) {
        console.error('Parse error:', err);
      } finally {
        setIsParsing(false);
      }
    },
    []
  );

  // Debounce pattern text edits
  useEffect(() => {
    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current);
    }
    debounceTimerRef.current = window.setTimeout(() => {
      runParseAndLayout(patternText, patternTitle, terminology);
    }, 350);

    return () => {
      if (debounceTimerRef.current) clearTimeout(debounceTimerRef.current);
    };
  }, [patternText, patternTitle, terminology, runParseAndLayout]);

  // Handle PDF or File Upload
  const handleFileUpload = async (file: File) => {
    try {
      setIsParsing(true);
      const title = file.name.replace(/\.[^/.]+$/, '');
      const parseRes = await ApiService.parseFile(file, title, terminology);
      setPatternTitle(title);
      setAst(parseRes.ast);
      setValidation(parseRes.validation);
      if (parseRes.ast?.raw_text) {
        setPatternText(parseRes.ast.raw_text);
      }

      const chartRes = await ApiService.generateChart(parseRes.ast, undefined, terminology);
      setChart(chartRes);
    } catch (err: any) {
      alert(`File upload error: ${err.message || err}`);
    } finally {
      setIsParsing(false);
    }
  };

  // Load Preset Sample
  const handleSelectSample = (sample: SamplePattern) => {
    setPatternTitle(sample.title);
    setPatternText(sample.pattern_text);
    setTerminology(sample.terminology || 'US');
    setCurrentStep(-1);
    setIsPlaying(false);
  };

  // Load Saved Project
  const handleLoadProject = (project: DBProject) => {
    setPatternTitle(project.title);
    setPatternText(project.raw_pattern);
    setTerminology((project.terminology as TerminologyStandard) || 'US');
    setCurrentStep(-1);
    setIsPlaying(false);
  };

  // Apply diagnostic suggestion
  const handleApplyFix = (suggestion: string) => {
    alert(`Suggestion: ${suggestion}`);
  };

  // Safely extract diagnostic items
  const diagnosticItems = validation?.diagnostics || validation?.issues || [];
  const errorCount = validation?.errors_count ?? validation?.error_count ?? 0;
  const totalDiagnosticsCount = validation?.total_diagnostics ?? diagnosticItems.length;

  // Active step details for playback
  const nodes = chart?.nodes || [];
  const activeNode = nodes.length > 0 && currentStep >= 0 && currentStep < nodes.length ? nodes[currentStep] : null;

  return (
    <div className={`app-container ${theme === 'light' ? 'theme-light' : ''}`}>
      {/* Top Navbar */}
      <header className="app-navbar">
        <div className="navbar-brand">
          <div className="brand-icon">
            <Sparkles size={20} />
          </div>
          <h1 className="brand-title">Crochart Visualizer</h1>
          <span className="brand-badge">Studio</span>
        </div>

        <div className="navbar-actions">
          {/* Presets Gallery */}
          <button className="nav-btn" onClick={() => setGalleryOpen(true)} title="Browse Pattern Presets">
            <BookOpen size={16} />
            <span>Preset Gallery</span>
          </button>

          {/* Saved Projects */}
          <button className="nav-btn" onClick={() => setProjectsOpen(true)} title="Save / Open Projects">
            <FolderArchive size={16} />
            <span>Projects</span>
          </button>

          {/* ML Studio */}
          <button className="nav-btn" onClick={() => setMlStudioOpen(true)} title="Synthetic Datasets & ML Benchmark">
            <BrainCircuit size={16} />
            <span>ML Studio</span>
          </button>

          {/* Export */}
          <button
            className="nav-btn primary"
            onClick={() => setExportOpen(true)}
            disabled={!chart || nodes.length === 0}
            title="Export Vector SVG, PNG, PDF or JSON"
          >
            <Download size={16} />
            <span>Export Chart</span>
          </button>

          {/* Theme Toggle */}
          <button
            className="icon-btn"
            onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
            title="Toggle Light / Dark Theme"
          >
            {theme === 'dark' ? <Sun size={17} /> : <Moon size={17} />}
          </button>
        </div>
      </header>

      {/* Main Workspace Split Layout */}
      <main className="workspace-body">
        {/* Left Pane: Editor & Diagnostics */}
        <section className="left-pane">
          <div className="sidebar-tab-header">
            <button
              className={`sidebar-tab-btn ${sidebarTab === 'editor' ? 'active' : ''}`}
              onClick={() => setSidebarTab('editor')}
            >
              <Edit3 size={15} />
              <span>Pattern Editor</span>
            </button>
            <button
              className={`sidebar-tab-btn ${sidebarTab === 'diagnostics' ? 'active' : ''}`}
              onClick={() => setSidebarTab('diagnostics')}
            >
              <AlertTriangle size={15} />
              <span>Diagnostics</span>
              {totalDiagnosticsCount > 0 && (
                <span className="badge-counter">{totalDiagnosticsCount}</span>
              )}
            </button>
          </div>

          <div className="pane-content-scroll">
            {sidebarTab === 'editor' ? (
              <PatternEditor
                patternText={patternText}
                onChangePattern={setPatternText}
                patternTitle={patternTitle}
                onChangeTitle={setPatternTitle}
                terminology={terminology}
                onChangeTerminology={setTerminology}
                onFileUpload={handleFileUpload}
                isParsing={isParsing}
                isValid={validation?.is_valid ?? true}
                errorCount={errorCount}
              />
            ) : (
              <ValidationPanel
                validation={validation}
                ast={ast}
                onApplyFix={handleApplyFix}
              />
            )}
          </div>
        </section>

        {/* Right Pane: Interactive Vector Canvas */}
        <section className="right-pane">
          <ChartCanvas
            chart={chart}
            selectedNode={selectedNode}
            onSelectNode={setSelectedNode}
            activeStep={currentStep}
            isPlaybackActive={currentStep >= 0}
          />

          {/* Bottom Stitch-by-Stitch Playback Animator */}
          {nodes.length > 0 && (
            <PlaybackControls
              totalSteps={nodes.length}
              currentStep={currentStep >= 0 ? currentStep : nodes.length - 1}
              onStepChange={setCurrentStep}
              isPlaying={isPlaying}
              onTogglePlay={() => {
                if (!isPlaying && (currentStep < 0 || currentStep >= nodes.length - 1)) {
                  setCurrentStep(0);
                }
                setIsPlaying(!isPlaying);
              }}
              activeRound={activeNode?.unit_index || activeNode?.unit_number}
              activeStitchType={activeNode?.stitch_type}
            />
          )}
        </section>
      </main>

      {/* Modals */}
      <SampleGallery
        isOpen={galleryOpen}
        onClose={() => setGalleryOpen(false)}
        samples={samples}
        onSelectSample={handleSelectSample}
      />

      <ProjectsModal
        isOpen={projectsOpen}
        onClose={() => setProjectsOpen(false)}
        currentTitle={patternTitle}
        currentPattern={patternText}
        currentTerminology={terminology}
        currentIsCircular={chart?.is_circular ?? true}
        currentAst={ast}
        currentChart={chart}
        onLoadProject={handleLoadProject}
      />

      <ExportModal
        isOpen={exportOpen}
        onClose={() => setExportOpen(false)}
        chart={chart}
        ast={ast}
        patternTitle={patternTitle}
      />

      <MLStudioModal
        isOpen={mlStudioOpen}
        onClose={() => setMlStudioOpen(false)}
        onLoadSyntheticPattern={(text, title) => {
          setPatternTitle(title);
          setPatternText(text);
          setCurrentStep(-1);
          setIsPlaying(false);
        }}
      />
    </div>
  );
};

export default App;
