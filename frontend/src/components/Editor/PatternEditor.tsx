import React, { useRef, useState } from 'react';
import { TerminologyStandard } from '../../types';
import {
  UploadCloud,
  FileText,
  Wand2,
  HelpCircle,
  CheckCircle2,
  AlertCircle,
  Copy,
  Trash2
} from 'lucide-react';

interface PatternEditorProps {
  patternText: string;
  onChangePattern: (text: string) => void;
  patternTitle: string;
  onChangeTitle: (title: string) => void;
  terminology: TerminologyStandard;
  onChangeTerminology: (term: TerminologyStandard) => void;
  onFileUpload: (file: File) => void;
  isParsing: boolean;
  isValid: boolean;
  errorCount: number;
}

const QUICK_INSERTS = [
  { label: 'MR 6 sc', snippet: 'MR 6 sc' },
  { label: 'inc', snippet: 'inc' },
  { label: 'sc', snippet: 'sc' },
  { label: 'dc', snippet: 'dc' },
  { label: 'hdc', snippet: 'hdc' },
  { label: 'ch', snippet: 'ch' },
  { label: 'sl st', snippet: 'sl st' },
  { label: '[ ... ] x 6', snippet: '[sc, inc] x 6' },
  { label: 'Rnd 1:', snippet: 'Rnd 1: ' }
];

export const PatternEditor: React.FC<PatternEditorProps> = ({
  patternText,
  onChangePattern,
  patternTitle,
  onChangeTitle,
  terminology,
  onChangeTerminology,
  onFileUpload,
  isParsing,
  isValid,
  errorCount
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const [isDraggingFile, setIsDraggingFile] = useState(false);

  const insertSnippet = (snippet: string) => {
    if (!textareaRef.current) return;
    const textarea = textareaRef.current;
    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const before = patternText.substring(0, start);
    const after = patternText.substring(end);
    const newText = before + snippet + after;
    onChangePattern(newText);

    setTimeout(() => {
      textarea.focus();
      textarea.setSelectionRange(start + snippet.length, start + snippet.length);
    }, 50);
  };

  const handleFileDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDraggingFile(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      onFileUpload(e.dataTransfer.files[0]);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(patternText);
  };

  const handleClear = () => {
    if (window.confirm('Clear current pattern text?')) {
      onChangePattern('');
    }
  };

  return (
    <div className="pattern-editor-container">
      {/* Editor Header */}
      <div className="editor-header">
        <div className="title-input-wrap">
          <input
            type="text"
            className="pattern-title-input"
            value={patternTitle}
            onChange={e => onChangeTitle(e.target.value)}
            placeholder="Pattern Title..."
          />
        </div>

        {/* Terminology Toggle */}
        <div className="terminology-toggle" title="Switch Between US and UK Crochet Terms">
          <button
            type="button"
            className={`term-btn ${terminology === 'US' ? 'active' : ''}`}
            onClick={() => onChangeTerminology('US')}
          >
            US Terms
          </button>
          <button
            type="button"
            className={`term-btn ${terminology === 'UK' ? 'active' : ''}`}
            onClick={() => onChangeTerminology('UK')}
          >
            UK Terms
          </button>
        </div>
      </div>

      {/* Quick Insert Symbol Bar */}
      <div className="quick-insert-bar">
        <span className="insert-label">Quick Insert:</span>
        <div className="insert-chips-scroll">
          {QUICK_INSERTS.map(item => (
            <button
              key={item.label}
              type="button"
              className="insert-chip"
              onClick={() => insertSnippet(item.snippet)}
            >
              {item.label}
            </button>
          ))}
        </div>
      </div>

      {/* Main Textarea Area */}
      <div
        className={`editor-body ${isDraggingFile ? 'drag-over' : ''}`}
        onDragOver={e => {
          e.preventDefault();
          setIsDraggingFile(true);
        }}
        onDragLeave={() => setIsDraggingFile(false)}
        onDrop={handleFileDrop}
      >
        <textarea
          ref={textareaRef}
          className="pattern-textarea"
          value={patternText}
          onChange={e => onChangePattern(e.target.value)}
          placeholder={`Enter or paste crochet pattern instructions...\n\nExample:\nRnd 1: MR 6 sc (6)\nRnd 2: 6 inc (12)\nRnd 3: [sc, inc] x 6 (18)\nRnd 4: [2 sc, inc] x 6 (24)`}
          spellCheck={false}
        />

        {/* Drag Drop Overlay */}
        {isDraggingFile && (
          <div className="drag-drop-overlay">
            <UploadCloud size={48} className="animate-bounce" />
            <p>Drop PDF or Pattern Text file to parse</p>
          </div>
        )}
      </div>

      {/* Editor Footer / Action Bar */}
      <div className="editor-footer">
        <div className="status-indicators">
          {isParsing ? (
            <span className="status-badge parsing">
              <span className="spinner-dot" /> Parsing...
            </span>
          ) : isValid ? (
            <span className="status-badge valid">
              <CheckCircle2 size={13} /> Valid Syntax
            </span>
          ) : (
            <span className="status-badge error">
              <AlertCircle size={13} /> {errorCount} {errorCount === 1 ? 'issue' : 'issues'}
            </span>
          )}
        </div>

        <div className="editor-actions">
          <input
            type="file"
            ref={fileInputRef}
            style={{ display: 'none' }}
            accept=".pdf,.txt,.crochet"
            onChange={e => {
              if (e.target.files && e.target.files.length > 0) {
                onFileUpload(e.target.files[0]);
              }
            }}
          />
          <button
            type="button"
            className="action-btn"
            onClick={() => fileInputRef.current?.click()}
            title="Upload Pattern PDF or TXT"
          >
            <UploadCloud size={14} />
            <span>Upload PDF/TXT</span>
          </button>
          <button
            type="button"
            className="action-btn"
            onClick={handleCopy}
            title="Copy Text to Clipboard"
          >
            <Copy size={14} />
          </button>
          <button
            type="button"
            className="action-btn danger"
            onClick={handleClear}
            title="Clear Pattern"
          >
            <Trash2 size={14} />
          </button>
        </div>
      </div>
    </div>
  );
};
