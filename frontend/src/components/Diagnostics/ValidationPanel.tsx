import React, { useState } from 'react';
import { ValidationReport, CrochetPatternAST } from '../../types';
import {
  AlertTriangle,
  AlertOctagon,
  CheckCircle,
  Code2,
  Table,
  Wand2,
  ChevronDown,
  ChevronRight,
  Info
} from 'lucide-react';

interface ValidationPanelProps {
  validation: ValidationReport | null;
  ast: CrochetPatternAST | null;
  onApplyFix?: (suggestion: string) => void;
}

export const ValidationPanel: React.FC<ValidationPanelProps> = ({
  validation,
  ast,
  onApplyFix
}) => {
  const [activeTab, setActiveTab] = useState<'issues' | 'stitch-math' | 'ast'>('issues');
  const [expandedNodes, setExpandedNodes] = useState<Record<string, boolean>>({ 'root': true });

  const toggleExpand = (id: string) => {
    setExpandedNodes(prev => ({ ...prev, [id]: !prev[id] }));
  };

  const diagnostics = validation?.diagnostics || validation?.issues || [];
  const errorsCount = validation?.errors_count ?? validation?.error_count ?? 0;
  const mathEntries = Object.entries(validation?.expected_vs_actual || {});

  return (
    <div className="validation-panel-container">
      {/* Tab Navigation */}
      <div className="panel-tab-bar">
        <button
          className={`panel-tab ${activeTab === 'issues' ? 'active' : ''}`}
          onClick={() => setActiveTab('issues')}
        >
          <div className="tab-title-wrap">
            <AlertTriangle size={14} />
            <span>Diagnostics</span>
            {diagnostics.length > 0 && (
              <span className={`issue-count-badge ${errorsCount > 0 ? 'has-errors' : 'has-warnings'}`}>
                {diagnostics.length}
              </span>
            )}
          </div>
        </button>

        <button
          className={`panel-tab ${activeTab === 'stitch-math' ? 'active' : ''}`}
          onClick={() => setActiveTab('stitch-math')}
        >
          <div className="tab-title-wrap">
            <Table size={14} />
            <span>Stitch Math</span>
          </div>
        </button>

        <button
          className={`panel-tab ${activeTab === 'ast' ? 'active' : ''}`}
          onClick={() => setActiveTab('ast')}
        >
          <div className="tab-title-wrap">
            <Code2 size={14} />
            <span>AST Tree</span>
          </div>
        </button>
      </div>

      {/* Tab Content */}
      <div className="panel-tab-content">
        {/* TAB 1: Issues & Diagnostics */}
        {activeTab === 'issues' && (
          <div className="issues-tab-body">
            {diagnostics.length === 0 ? (
              <div className="all-clean-state">
                <CheckCircle size={32} className="text-emerald" />
                <h4>Perfect Pattern Math!</h4>
                <p>No stitch count discrepancies or syntax errors detected.</p>
              </div>
            ) : (
              <div className="issue-list">
                {diagnostics.map((diag, idx) => {
                  const isError = diag.severity === 'error';
                  const unitNum = diag.unit_index || diag.unit_number;
                  const fix = diag.suggested_fix || diag.suggestion;
                  return (
                    <div key={idx} className={`issue-card ${diag.severity || 'warning'}`}>
                      <div className="issue-card-header">
                        <div className="issue-title-group">
                          {isError ? (
                            <AlertOctagon size={16} className="text-rose" />
                          ) : (
                            <AlertTriangle size={16} className="text-amber" />
                          )}
                          <span className="issue-rule-code">{diag.rule_code}</span>
                          {unitNum && (
                            <span className="issue-unit-tag">Round {unitNum}</span>
                          )}
                        </div>
                      </div>

                      <p className="issue-message">{diag.message}</p>

                      {fix && (
                        <div className="issue-suggestion-box">
                          <div className="suggestion-text">
                            <strong>Tip:</strong> {fix}
                          </div>
                          {onApplyFix && (
                            <button
                              className="apply-fix-btn"
                              onClick={() => onApplyFix(fix)}
                              title="Auto-apply recommendation"
                            >
                              <Wand2 size={12} />
                              <span>Apply Fix</span>
                            </button>
                          )}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}

        {/* TAB 2: Stitch Math Verification */}
        {activeTab === 'stitch-math' && (
          <div className="stitch-math-body">
            {mathEntries.length === 0 ? (
              <div className="math-empty-state">
                <Info size={24} />
                <p>No round stitch counts calculated yet.</p>
              </div>
            ) : (
              <table className="math-table">
                <thead>
                  <tr>
                    <th>Unit</th>
                    <th>Calculated Stitches</th>
                    <th>Claimed / Expected</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {mathEntries.map(([unitKey, counts]) => {
                    const match = counts.expected === counts.actual;
                    return (
                      <tr key={unitKey} className={match ? 'row-match' : 'row-mismatch'}>
                        <td className="unit-col"><strong>Round {unitKey}</strong></td>
                        <td className="actual-col">{counts.actual} sts</td>
                        <td className="expected-col">{counts.expected || '—'} sts</td>
                        <td className="status-col">
                          {match ? (
                            <span className="math-badge match">Balanced</span>
                          ) : (
                            <span className="math-badge mismatch">
                              Δ {counts.actual - counts.expected > 0 ? `+${counts.actual - counts.expected}` : counts.actual - counts.expected}
                            </span>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            )}
          </div>
        )}

        {/* TAB 3: AST Syntax Tree View */}
        {activeTab === 'ast' && (
          <div className="ast-tree-body">
            {ast ? (
              <div className="ast-tree">
                <div className="ast-root-node">
                  <div className="node-label" onClick={() => toggleExpand('root')}>
                    {expandedNodes['root'] ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                    <span className="node-type">PatternAST:</span> <strong>{ast.title}</strong>
                    <span className="node-meta">({ast.units?.length || 0} units, {ast.terminology})</span>
                  </div>

                  {expandedNodes['root'] && ast.units && (
                    <div className="tree-children">
                      {ast.units.map(u => {
                        const unitNum = u.index || (u as any).unit_number || 1;
                        const unitId = `unit-${unitNum}`;
                        const isExpanded = expandedNodes[unitId];
                        return (
                          <div key={unitId} className="tree-unit-node">
                            <div className="node-label" onClick={() => toggleExpand(unitId)}>
                              {isExpanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                              <span className="node-unit-tag">{u.unit_type} {unitNum}</span>
                              <span className="node-meta">({u.instructions?.length || 0} instructions)</span>
                            </div>

                            {isExpanded && (
                              <div className="tree-instructions">
                                {u.instructions?.map((inst: any, iIdx: number) => (
                                  <div key={iIdx} className="tree-instruction-item">
                                    <div className="inst-raw">"{inst.raw_text || inst.id || 'instruction'}"</div>
                                    {inst.repeat_count && inst.repeat_count > 1 && (
                                      <span className="repeat-tag">repeat x{inst.repeat_count}</span>
                                    )}
                                    {inst.stitch_type && (
                                      <div className="inst-stitches">
                                        <span className="stitch-chip">
                                          {inst.count || 1}x {inst.stitch_type}
                                        </span>
                                      </div>
                                    )}
                                  </div>
                                ))}
                              </div>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div className="math-empty-state">
                <Code2 size={24} />
                <p>No AST generated yet.</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
