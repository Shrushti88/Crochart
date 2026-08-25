import React, { useState } from 'react';
import { ApiService } from '../../services/api';
import {
  BrainCircuit,
  X,
  Play,
  CheckCircle,
  BarChart3,
  Sparkles,
  Zap,
  Activity,
  Layers
} from 'lucide-react';

interface MLStudioModalProps {
  isOpen: boolean;
  onClose: () => void;
  onLoadSyntheticPattern: (patternText: string, title: string) => void;
}

export const MLStudioModal: React.FC<MLStudioModalProps> = ({
  isOpen,
  onClose,
  onLoadSyntheticPattern
}) => {
  const [category, setCategory] = useState<string>('all');
  const [count, setCount] = useState<number>(5);
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedSamples, setGeneratedSamples] = useState<any[]>([]);
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [evalReport, setEvalReport] = useState<any>(null);

  if (!isOpen) return null;

  const handleGenerate = async () => {
    try {
      setIsGenerating(true);
      const res = await ApiService.generateSynthetic(count, category);
      setGeneratedSamples(res.samples || []);
    } catch (err) {
      alert('Failed to generate synthetic dataset');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleEvaluate = async () => {
    try {
      setIsEvaluating(true);
      const report = await ApiService.evaluateML(generatedSamples.length > 0 ? generatedSamples : undefined);
      setEvalReport(report);
    } catch (err) {
      alert('Evaluation failed');
    } finally {
      setIsEvaluating(false);
    }
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-content ml-modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title-wrap">
            <BrainCircuit size={20} className="text-primary" />
            <h2>ML Synthetic Dataset & Evaluation Studio</h2>
          </div>
          <button className="modal-close-btn" onClick={onClose}>
            <X size={18} />
          </button>
        </div>

        <p className="ml-intro">
          Generate rule-compliant synthetic crochet datasets with ground-truth ASTs to benchmark parser robustness and ML accuracy.
        </p>

        {/* Generator Controls */}
        <div className="ml-controls-card">
          <div className="control-field">
            <label>Archetype Category:</label>
            <select
              value={category}
              onChange={e => setCategory(e.target.value)}
              className="ml-select"
            >
              <option value="all">All Archetypes (Mixed)</option>
              <option value="amigurumi">Amigurumi 3D Spheres</option>
              <option value="flat_circle">Flat Circular Mandalas</option>
              <option value="row_fabric">Row-by-Row Fabrics</option>
            </select>
          </div>

          <div className="control-field">
            <label>Sample Count:</label>
            <input
              type="number"
              min="1"
              max="25"
              value={count}
              onChange={e => setCount(parseInt(e.target.value, 10))}
              className="ml-input-num"
            />
          </div>

          <div className="ml-btn-group">
            <button
              className="btn-primary"
              onClick={handleGenerate}
              disabled={isGenerating}
            >
              <Sparkles size={16} />
              <span>{isGenerating ? 'Generating...' : 'Generate Batch'}</span>
            </button>
            <button
              className="btn-secondary"
              onClick={handleEvaluate}
              disabled={isEvaluating}
            >
              <Play size={16} />
              <span>{isEvaluating ? 'Evaluating...' : 'Run Benchmark'}</span>
            </button>
          </div>
        </div>

        {/* Evaluation Metrics Card */}
        {evalReport && (
          <div className="eval-metrics-card">
            <h3>
              <Activity size={18} />
              <span>Benchmark Results ({evalReport.total_samples} samples)</span>
            </h3>

            <div className="metrics-grid">
              <div className="metric-stat">
                <span className="stat-label">Parse Success Rate</span>
                <span className="stat-value text-emerald">
                  {(evalReport.parse_success_rate * 100).toFixed(1)}%
                </span>
              </div>
              <div className="metric-stat">
                <span className="stat-label">Avg Units / Pattern</span>
                <span className="stat-value">{evalReport.avg_units_per_pattern?.toFixed(1) || '0'}</span>
              </div>
              <div className="metric-stat">
                <span className="stat-label">Avg Stitches / Pattern</span>
                <span className="stat-value">{evalReport.avg_stitches_per_pattern?.toFixed(1) || '0'}</span>
              </div>
            </div>
          </div>
        )}

        {/* Generated Samples List */}
        {generatedSamples.length > 0 && (
          <div className="generated-samples-section">
            <h3>Generated Synthetic Patterns ({generatedSamples.length})</h3>
            <div className="synthetic-list">
              {generatedSamples.map((sample, idx) => (
                <div key={idx} className="synthetic-item">
                  <div className="synthetic-top">
                    <span className="synthetic-badge">{sample.archetype || 'Synthetic'}</span>
                    <button
                      className="load-synthetic-btn"
                      onClick={() => {
                        onLoadSyntheticPattern(sample.written_pattern, `Synthetic Pattern #${idx + 1}`);
                        onClose();
                      }}
                    >
                      Load into Visualizer
                    </button>
                  </div>
                  <pre className="synthetic-code">{sample.written_pattern}</pre>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
