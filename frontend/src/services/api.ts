import {
  CrochetPatternAST,
  ValidationReport,
  ChartGraph,
  ParseResponse,
  SamplePattern,
  DBProject,
  TerminologyStandard
} from '../types';

const API_BASE = '/api/v1';

export const ApiService = {
  // Parse text pattern
  async parseText(patternText: string, title?: string, terminology: TerminologyStandard = 'US'): Promise<ParseResponse> {
    const res = await fetch(`${API_BASE}/parse/text`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        pattern_text: patternText,
        title: title || 'Crochet Pattern',
        terminology
      })
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Failed to parse pattern' }));
      throw new Error(err.detail || 'Failed to parse pattern');
    }
    return res.json();
  },

  // Parse uploaded file (PDF / Text)
  async parseFile(file: File, title?: string, terminology: TerminologyStandard = 'US'): Promise<ParseResponse> {
    const formData = new FormData();
    formData.append('file', file);
    if (title) formData.append('title', title);
    formData.append('terminology', terminology);

    const res = await fetch(`${API_BASE}/parse/file`, {
      method: 'POST',
      body: formData
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Failed to parse uploaded file' }));
      throw new Error(err.detail || 'Failed to parse uploaded file');
    }
    return res.json();
  },

  // Generate interactive chart graph
  async generateChart(ast?: CrochetPatternAST, patternText?: string, terminology: TerminologyStandard = 'US'): Promise<ChartGraph> {
    const res = await fetch(`${API_BASE}/chart/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ast,
        pattern_text: patternText,
        terminology
      })
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Failed to generate chart graph' }));
      throw new Error(err.detail || 'Failed to generate chart graph');
    }
    return res.json();
  },

  // Sample Patterns
  async getSamples(): Promise<SamplePattern[]> {
    const res = await fetch(`${API_BASE}/samples`);
    if (!res.ok) throw new Error('Failed to load sample patterns');
    return res.json();
  },

  async getSampleById(id: string): Promise<SamplePattern> {
    const res = await fetch(`${API_BASE}/samples/${id}`);
    if (!res.ok) throw new Error('Sample not found');
    return res.json();
  },

  // Projects CRUD
  async listProjects(): Promise<DBProject[]> {
    const res = await fetch(`${API_BASE}/projects`);
    if (!res.ok) throw new Error('Failed to fetch projects');
    return res.json();
  },

  async createProject(project: Partial<DBProject>): Promise<DBProject> {
    const res = await fetch(`${API_BASE}/projects`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(project)
    });
    if (!res.ok) throw new Error('Failed to save project');
    return res.json();
  },

  async deleteProject(id: number): Promise<void> {
    const res = await fetch(`${API_BASE}/projects/${id}`, {
      method: 'DELETE'
    });
    if (!res.ok) throw new Error('Failed to delete project');
  },

  // Export
  async exportChart(format: 'svg' | 'json' | 'pdf', chart: ChartGraph, title: string): Promise<Blob> {
    const res = await fetch(`${API_BASE}/export`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chart,
        format,
        title
      })
    });
    if (!res.ok) throw new Error('Export failed');
    return res.blob();
  },

  // Synthetic datasets & ML evaluation
  async generateSynthetic(count: number = 5, category: string = 'all'): Promise<{ count: number; samples: any[] }> {
    const res = await fetch(`${API_BASE}/datasets/generate-synthetic`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ count, category, save_to_db: true })
    });
    if (!res.ok) throw new Error('Failed to generate synthetic data');
    return res.json();
  },

  async evaluateML(samples?: any[]): Promise<any> {
    const res = await fetch(`${API_BASE}/datasets/evaluate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ samples, use_db_samples: !samples })
    });
    if (!res.ok) throw new Error('Failed to evaluate dataset');
    return res.json();
  }
};
