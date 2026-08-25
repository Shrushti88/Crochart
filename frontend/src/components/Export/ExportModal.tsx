import React, { useState } from 'react';
import { ChartGraph, CrochetPatternAST } from '../../types';
import { ApiService } from '../../services/api';
import {
  Download,
  FileImage,
  FileText,
  Code,
  X,
  Check,
  Sparkles
} from 'lucide-react';

interface ExportModalProps {
  isOpen: boolean;
  onClose: () => void;
  chart: ChartGraph | null;
  ast: CrochetPatternAST | null;
  patternTitle: string;
}

export const ExportModal: React.FC<ExportModalProps> = ({
  isOpen,
  onClose,
  chart,
  ast,
  patternTitle
}) => {
  const [exportingFormat, setExportingFormat] = useState<string | null>(null);

  if (!isOpen || !chart) return null;

  const downloadBlob = (blob: Blob, filename: string) => {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleExport = async (format: 'svg' | 'json' | 'pdf' | 'png') => {
    try {
      setExportingFormat(format);
      const safeTitle = (patternTitle || 'crochet_chart').replace(/[^a-z0-9_-]/gi, '_');

      if (format === 'png') {
        // Render SVG to canvas and export PNG
        const svgElement = document.querySelector('.canvas-svg') as SVGSVGElement;
        if (!svgElement) throw new Error('Canvas SVG not found');

        const serializer = new XMLSerializer();
        const svgString = serializer.serializeToString(svgElement);
        const svgBlob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
        const URLObj = window.URL || window.webkitURL || window;
        const blobURL = URLObj.createObjectURL(svgBlob);

        const image = new Image();
        image.onload = () => {
          const canvas = document.createElement('canvas');
          const padding = 60;
          canvas.width = image.width + padding * 2 || 1200;
          canvas.height = image.height + padding * 2 || 1200;
          const ctx = canvas.getContext('2d');
          if (ctx) {
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(image, padding, padding);

            // Title badge on PNG
            ctx.fillStyle = '#1e293b';
            ctx.font = 'bold 20px sans-serif';
            ctx.fillText(patternTitle || 'Crochet Chart', padding, 40);

            canvas.toBlob(blob => {
              if (blob) downloadBlob(blob, `${safeTitle}.png`);
            }, 'image/png');
          }
          URLObj.revokeObjectURL(blobURL);
        };
        image.src = blobURL;
        return;
      }

      // Backend export for SVG, JSON, PDF
      const blob = await ApiService.exportChart(format, chart, safeTitle);
      downloadBlob(blob, `${safeTitle}.${format}`);
    } catch (err) {
      alert(`Export failed for format ${format}`);
    } finally {
      setExportingFormat(null);
    }
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-content export-modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title-wrap">
            <Download size={20} className="text-primary" />
            <h2>Export Crochet Diagram</h2>
          </div>
          <button className="modal-close-btn" onClick={onClose}>
            <X size={18} />
          </button>
        </div>

        <p className="export-intro">
          Choose your desired export format for <strong>"{patternTitle}"</strong>:
        </p>

        <div className="export-options-grid">
          {/* Option 1: Vector SVG */}
          <div className="export-card" onClick={() => handleExport('svg')}>
            <div className="export-icon svg-icon">
              <FileImage size={28} />
            </div>
            <div className="export-card-content">
              <h4>Scalable Vector Graphics (SVG)</h4>
              <p>Crisp vector format suitable for Illustrator, Inkscape, or high-res web publishing.</p>
            </div>
            <button className="btn-export" disabled={exportingFormat === 'svg'}>
              {exportingFormat === 'svg' ? 'Exporting...' : 'Export SVG'}
            </button>
          </div>

          {/* Option 2: High-Res PNG */}
          <div className="export-card" onClick={() => handleExport('png')}>
            <div className="export-icon png-icon">
              <FileImage size={28} />
            </div>
            <div className="export-card-content">
              <h4>High-Resolution PNG</h4>
              <p>Ready to share on social media, blogs, or pattern documents with clean white background.</p>
            </div>
            <button className="btn-export" disabled={exportingFormat === 'png'}>
              {exportingFormat === 'png' ? 'Exporting...' : 'Export PNG'}
            </button>
          </div>

          {/* Option 3: PDF Document */}
          <div className="export-card" onClick={() => handleExport('pdf')}>
            <div className="export-icon pdf-icon">
              <FileText size={28} />
            </div>
            <div className="export-card-content">
              <h4>Printable PDF Document</h4>
              <p>Formatted pattern sheet with stitch statistics and metadata ready for printing.</p>
            </div>
            <button className="btn-export" disabled={exportingFormat === 'pdf'}>
              {exportingFormat === 'pdf' ? 'Exporting...' : 'Export PDF'}
            </button>
          </div>

          {/* Option 4: JSON AST & Layout */}
          <div className="export-card" onClick={() => handleExport('json')}>
            <div className="export-icon json-icon">
              <Code size={28} />
            </div>
            <div className="export-card-content">
              <h4>Structured JSON (AST & Nodes)</h4>
              <p>Complete syntax tree, node coordinates, links, and validation metadata for developer use.</p>
            </div>
            <button className="btn-export" disabled={exportingFormat === 'json'}>
              {exportingFormat === 'json' ? 'Exporting...' : 'Export JSON'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
