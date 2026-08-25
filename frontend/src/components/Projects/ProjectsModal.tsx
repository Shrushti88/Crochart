import React, { useState, useEffect } from 'react';
import { DBProject, CrochetPatternAST, ChartGraph } from '../../types';
import { ApiService } from '../../services/api';
import {
  FolderArchive,
  Save,
  Trash2,
  Download,
  Plus,
  X,
  FileCode,
  Calendar,
  Check
} from 'lucide-react';

interface ProjectsModalProps {
  isOpen: boolean;
  onClose: () => void;
  currentTitle: string;
  currentPattern: string;
  currentTerminology: string;
  currentIsCircular: boolean;
  currentAst: CrochetPatternAST | null;
  currentChart: ChartGraph | null;
  onLoadProject: (project: DBProject) => void;
}

export const ProjectsModal: React.FC<ProjectsModalProps> = ({
  isOpen,
  onClose,
  currentTitle,
  currentPattern,
  currentTerminology,
  currentIsCircular,
  currentAst,
  currentChart,
  onLoadProject
}) => {
  const [projects, setProjects] = useState<DBProject[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [saveTitle, setSaveTitle] = useState(currentTitle);
  const [saveDesc, setSaveDesc] = useState('');
  const [isSaving, setIsSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);

  const fetchProjects = async () => {
    try {
      setIsLoading(true);
      const data = await ApiService.listProjects();
      setProjects(data);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      setSaveTitle(currentTitle);
      fetchProjects();
    }
  }, [isOpen, currentTitle]);

  if (!isOpen) return null;

  const handleSaveCurrent = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!saveTitle.trim()) return;

    try {
      setIsSaving(true);
      await ApiService.createProject({
        title: saveTitle,
        description: saveDesc,
        raw_pattern: currentPattern,
        terminology: currentTerminology,
        is_circular: currentIsCircular,
        ast_data: currentAst || undefined,
        chart_data: currentChart || undefined
      });
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 2500);
      setSaveDesc('');
      await fetchProjects();
    } catch (err) {
      alert('Failed to save project');
    } finally {
      setIsSaving(false);
    }
  };

  const handleDelete = async (id: number, e: React.MouseEvent) => {
    e.stopPropagation();
    if (window.confirm('Delete this saved project?')) {
      try {
        await ApiService.deleteProject(id);
        setProjects(prev => prev.filter(p => p.id !== id));
      } catch (err) {
        alert('Failed to delete project');
      }
    }
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-content projects-modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title-wrap">
            <FolderArchive size={20} className="text-primary" />
            <h2>Saved Projects & Patterns</h2>
          </div>
          <button className="modal-close-btn" onClick={onClose}>
            <X size={18} />
          </button>
        </div>

        {/* Save Current Pattern Card */}
        <form className="save-current-form" onSubmit={handleSaveCurrent}>
          <h3>Save Active Pattern</h3>
          <div className="form-row">
            <input
              type="text"
              placeholder="Project Name..."
              value={saveTitle}
              onChange={e => setSaveTitle(e.target.value)}
              className="form-input"
              required
            />
            <input
              type="text"
              placeholder="Optional notes / yarn type..."
              value={saveDesc}
              onChange={e => setSaveDesc(e.target.value)}
              className="form-input"
            />
            <button type="submit" className="btn-primary" disabled={isSaving}>
              {saveSuccess ? <Check size={16} /> : <Save size={16} />}
              <span>{saveSuccess ? 'Saved!' : isSaving ? 'Saving...' : 'Save'}</span>
            </button>
          </div>
        </form>

        <hr className="modal-divider" />

        {/* Existing Projects List */}
        <div className="projects-list-wrap">
          <h3>Your Library ({projects.length})</h3>
          {isLoading ? (
            <div className="loading-state">Loading projects...</div>
          ) : projects.length === 0 ? (
            <div className="empty-projects">
              <FileCode size={32} />
              <p>No saved projects yet. Save your current pattern above!</p>
            </div>
          ) : (
            <div className="projects-grid">
              {projects.map(proj => (
                <div
                  key={proj.id}
                  className="saved-project-card"
                  onClick={() => {
                    onLoadProject(proj);
                    onClose();
                  }}
                >
                  <div className="proj-card-top">
                    <h4>{proj.title}</h4>
                    <button
                      className="delete-proj-btn"
                      onClick={e => handleDelete(proj.id, e)}
                      title="Delete Project"
                    >
                      <Trash2 size={13} />
                    </button>
                  </div>
                  {proj.description && <p className="proj-desc">{proj.description}</p>}
                  <div className="proj-meta">
                    <span className="meta-badge">{proj.terminology}</span>
                    <span className="meta-badge">{proj.is_circular ? 'Circular' : 'Row'}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
