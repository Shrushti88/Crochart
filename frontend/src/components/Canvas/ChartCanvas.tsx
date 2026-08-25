import React, { useState, useRef, useEffect, useCallback } from 'react';
import { ChartGraph, ChartNode } from '../../types';
import { RenderStitchSymbol } from './CYCSymbols';
import {
  ZoomIn,
  ZoomOut,
  Maximize2,
  RotateCcw,
  Eye,
  Layers,
  Palette,
  Grid,
  Info,
  Sparkles
} from 'lucide-react';

interface ChartCanvasProps {
  chart: ChartGraph | null;
  selectedNode: ChartNode | null;
  onSelectNode: (node: ChartNode | null) => void;
  activeStep?: number; // For step-by-step playback
  isPlaybackActive?: boolean;
}

export const COLOR_PALETTES = {
  traditional: {
    name: 'Traditional Diagram (Ref)',
    colors: ['#1e293b', '#1e293b', '#1e293b', '#1e293b', '#1e293b', '#1e293b', '#1e293b', '#1e293b']
  },
  jewel: {
    name: 'Jewel Yarn',
    colors: ['#6366f1', '#ec4899', '#10b981', '#f59e0b', '#8b5cf6', '#06b6d4', '#f43f5e', '#14b8a6']
  },
  sunset: {
    name: 'Sunset Wool',
    colors: ['#f97316', '#fb7185', '#e11d48', '#be123c', '#831843', '#4c0519', '#fb923c', '#fda4af']
  },
  forest: {
    name: 'Emerald Forest',
    colors: ['#10b981', '#059669', '#047857', '#065f46', '#34d399', '#6ee7b7', '#14b8a6', '#0d9488']
  },
  slate: {
    name: 'Monochrome Slate',
    colors: ['#94a3b8', '#64748b', '#475569', '#334155', '#cbd5e1', '#e2e8f0', '#0ea5e9', '#38bdf8']
  }
};

export const ChartCanvas: React.FC<ChartCanvasProps> = ({
  chart,
  selectedNode,
  onSelectNode,
  activeStep = -1,
  isPlaybackActive = false
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [transform, setTransform] = useState<{ x: number; y: number; scale: number }>({
    x: 0,
    y: 0,
    scale: 1
  });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState<{ x: number; y: number }>({ x: 0, y: 0 });

  // View settings
  const [showGrid, setShowGrid] = useState(true);
  const [showLinks, setShowLinks] = useState(false);
  const [showNumbers, setShowNumbers] = useState(false);
  const [showIncreaseHighlights, setShowIncreaseHighlights] = useState(true);
  const [selectedPalette, setSelectedPalette] = useState<keyof typeof COLOR_PALETTES>('traditional');
  const [hoveredNode, setHoveredNode] = useState<ChartNode | null>(null);

  // Auto-fit to view when new chart loads
  const fitToView = useCallback(() => {
    if (!chart || !containerRef.current) return;
    const { width: containerW, height: containerH } = containerRef.current.getBoundingClientRect();
    const b = chart.bounds;
    const chartW = Math.max(b.width, 100);
    const chartH = Math.max(b.height, 100);

    const padding = 60;
    const scaleX = (containerW - padding * 2) / chartW;
    const scaleY = (containerH - padding * 2) / chartH;
    const newScale = Math.min(Math.max(Math.min(scaleX, scaleY), 0.2), 3.5);

    const centerX = (b.min_x + b.max_x) / 2;
    const centerY = (b.min_y + b.max_y) / 2;

    setTransform({
      x: containerW / 2 - centerX * newScale,
      y: containerH / 2 - centerY * newScale,
      scale: newScale
    });
  }, [chart]);

  useEffect(() => {
    fitToView();
  }, [chart, fitToView]);

  // Pan handlers
  const handleMouseDown = (e: React.MouseEvent) => {
    if (e.button !== 0) return; // Only left click
    setIsDragging(true);
    setDragStart({ x: e.clientX - transform.x, y: e.clientY - transform.y });
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!isDragging) return;
    setTransform(prev => ({
      ...prev,
      x: e.clientX - dragStart.x,
      y: e.clientY - dragStart.y
    }));
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  // Zoom handlers
  const handleWheel = (e: React.WheelEvent) => {
    e.preventDefault();
    if (!containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;

    const zoomFactor = e.deltaY < 0 ? 1.15 : 0.87;
    const newScale = Math.min(Math.max(transform.scale * zoomFactor, 0.1), 8);

    const newX = mouseX - (mouseX - transform.x) * (newScale / transform.scale);
    const newY = mouseY - (mouseY - transform.y) * (newScale / transform.scale);

    setTransform({ x: newX, y: newY, scale: newScale });
  };

  const zoomIn = () => {
    setTransform(prev => ({ ...prev, scale: Math.min(prev.scale * 1.25, 8) }));
  };

  const zoomOut = () => {
    setTransform(prev => ({ ...prev, scale: Math.max(prev.scale * 0.8, 0.1) }));
  };

  const resetView = () => {
    fitToView();
  };

  // Filter nodes for playback animation
  const paletteColors = COLOR_PALETTES[selectedPalette].colors;
  const nodesToRender = chart?.nodes?.filter((_, idx) => {
    if (!isPlaybackActive || activeStep < 0) return true;
    return idx <= activeStep;
  }) || [];

  const nodeMap = new Map(chart?.nodes?.map(n => [n.id, n]) || []);

  const getNodeColor = (node: ChartNode) => {
    const unitNum = node.unit_index || node.unit_number || 1;
    const colorIndex = (unitNum - 1) % paletteColors.length;
    return paletteColors[Math.max(0, colorIndex)];
  };

  return (
    <div
      ref={containerRef}
      className="chart-canvas-container"
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
      onWheel={handleWheel}
    >
      {/* Floating Canvas Toolbar */}
      <div className="canvas-toolbar" onClick={e => e.stopPropagation()}>
        <div className="toolbar-group">
          <button className="tool-btn" onClick={zoomIn} title="Zoom In (+)">
            <ZoomIn size={16} />
          </button>
          <button className="tool-btn" onClick={zoomOut} title="Zoom Out (-)">
            <ZoomOut size={16} />
          </button>
          <button className="tool-btn" onClick={fitToView} title="Fit to View">
            <Maximize2 size={16} />
          </button>
          <button className="tool-btn" onClick={resetView} title="Reset View">
            <RotateCcw size={16} />
          </button>
        </div>

        <div className="toolbar-divider" />

        <div className="toolbar-group">
          <button
            className={`tool-btn ${showIncreaseHighlights ? 'active' : ''}`}
            onClick={() => setShowIncreaseHighlights(!showIncreaseHighlights)}
            title="Highlight Stacked Increases (Salmon Circles)"
          >
            <Sparkles size={16} />
          </button>
          <button
            className={`tool-btn ${showGrid ? 'active' : ''}`}
            onClick={() => setShowGrid(!showGrid)}
            title="Toggle Concentric Rings & Guides"
          >
            <Grid size={16} />
          </button>
          <button
            className={`tool-btn ${showLinks ? 'active' : ''}`}
            onClick={() => setShowLinks(!showLinks)}
            title="Toggle Stitch Connections & Chains"
          >
            <Layers size={16} />
          </button>
          <button
            className={`tool-btn ${showNumbers ? 'active' : ''}`}
            onClick={() => setShowNumbers(!showNumbers)}
            title="Toggle Stitch Index Numbers"
          >
            <Eye size={16} />
          </button>
        </div>

        <div className="toolbar-divider" />

        {/* Palette Selector */}
        <div className="toolbar-group palette-dropdown">
          <button className="tool-btn palette-btn" title="Change Color Palette">
            <Palette size={16} />
            <span className="palette-swatch" style={{ background: paletteColors[0] }} />
          </button>
          <div className="palette-menu">
            {Object.entries(COLOR_PALETTES).map(([key, pal]) => (
              <button
                key={key}
                className={`palette-option ${selectedPalette === key ? 'selected' : ''}`}
                onClick={() => setSelectedPalette(key as keyof typeof COLOR_PALETTES)}
              >
                <div className="palette-preview">
                  {pal.colors.slice(0, 4).map((c, i) => (
                    <span key={i} style={{ background: c }} />
                  ))}
                </div>
                <span>{pal.name}</span>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Scale Badge */}
      <div className="scale-indicator">
        {Math.round(transform.scale * 100)}%
      </div>

      {/* Main SVG Render Surface */}
      <svg
        className="canvas-svg"
        style={{
          cursor: isDragging ? 'grabbing' : 'grab'
        }}
      >
        <g transform={`translate(${transform.x}, ${transform.y}) scale(${transform.scale})`}>
          {/* Background Concentric Grid & Axis Guides for Circular Charts */}
          {chart && showGrid && chart.is_circular && (
            <g className="chart-guides" opacity="0.22">
              {/* Center crosshair */}
              <line x1="-1200" y1="0" x2="1200" y2="0" stroke="var(--border-color)" strokeDasharray="3 3" />
              <line x1="0" y1="-1200" x2="0" y2="1200" stroke="var(--border-color)" strokeDasharray="3 3" />

              {/* Radial angle rays for 6 sectors (every 60 deg) */}
              {[0, 60, 120, 180, 240, 300].map(angle => {
                const rad = ((angle - 90) * Math.PI) / 180;
                const x2 = Math.cos(rad) * 650;
                const y2 = Math.sin(rad) * 650;
                return (
                  <line
                    key={angle}
                    x1="0"
                    y1="0"
                    x2={x2}
                    y2={y2}
                    stroke="var(--border-color)"
                    strokeDasharray="2 4"
                  />
                );
              })}

              {/* Concentric Round rings */}
              {chart.round_radii &&
                Object.entries(chart.round_radii).map(([roundNum, radius]) => (
                  <g key={roundNum}>
                    <circle
                      cx="0"
                      cy="0"
                      r={radius}
                      fill="none"
                      stroke="var(--border-color)"
                      strokeWidth="1"
                      strokeDasharray="3 4"
                    />
                    <text
                      x={radius + 4}
                      y="-4"
                      fontSize="9"
                      fill="var(--text-muted)"
                      opacity="0.6"
                    >
                      R{roundNum}
                    </text>
                  </g>
                ))}
            </g>
          )}

          {/* Background Grid for Row / Linear Fabrics */}
          {chart && showGrid && !chart.is_circular && (
            <g className="chart-linear-guides" opacity="0.15">
              {Array.from({ length: 20 }).map((_, i) => (
                <line
                  key={i}
                  x1="-1000"
                  y1={i * 45}
                  x2="2000"
                  y2={i * 45}
                  stroke="var(--text-muted)"
                  strokeDasharray="2 4"
                />
              ))}
            </g>
          )}

          {/* Stitch Links & Connectors */}
          {chart && showLinks && (
            <g className="chart-links-layer">
              {chart.links?.map((link, idx) => {
                const src = nodeMap.get(link.source_id);
                const tgt = nodeMap.get(link.target_id);
                if (!src || !tgt) return null;

                // Only show links if both nodes are visible in playback
                if (isPlaybackActive && activeStep >= 0) {
                  const srcIdx = chart.nodes.findIndex(n => n.id === src.id);
                  const tgtIdx = chart.nodes.findIndex(n => n.id === tgt.id);
                  if (srcIdx > activeStep || tgtIdx > activeStep) return null;
                }

                const isJoin = link.link_type === 'join';
                return (
                  <line
                    key={`link-${idx}`}
                    x1={src.x}
                    y1={src.y}
                    x2={tgt.x}
                    y2={tgt.y}
                    stroke={isJoin ? '#f43f5e' : 'var(--chart-link-color)'}
                    strokeWidth={isJoin ? 2 : 1.2}
                    strokeDasharray={isJoin ? '4 3' : '2 2'}
                    opacity={isJoin ? 0.8 : 0.4}
                  />
                );
              })}
            </g>
          )}

          {/* Stitch Nodes Layer */}
          <g className="chart-nodes-layer">
            {nodesToRender.map((node, idx) => {
              const color = getNodeColor(node);
              const isSelected = selectedNode?.id === node.id;
              const isHovered = hoveredNode?.id === node.id;
              const isActivePlaybackNode = isPlaybackActive && activeStep === idx;
              const isIncrease = node.stitch_type === 'inc' || node.symbol_name.includes('inc');

              return (
                <g
                  key={node.id}
                  className={`stitch-node-group ${isSelected ? 'selected' : ''} ${isActivePlaybackNode ? 'active-step' : ''}`}
                  transform={`translate(${node.x}, ${node.y}) rotate(${node.rotation})`}
                  onClick={e => {
                    e.stopPropagation();
                    onSelectNode(isSelected ? null : node);
                  }}
                  onMouseEnter={() => setHoveredNode(node)}
                  onMouseLeave={() => setHoveredNode(null)}
                >
                  {/* Soft Salmon/Coral Circular Halo for Stacked Increases (as in traditional reference) */}
                  {showIncreaseHighlights && isIncrease && (
                    <circle
                      cx="0"
                      cy="0"
                      r="12"
                      fill="#f43f5e"
                      fillOpacity="0.22"
                      stroke="#f43f5e"
                      strokeWidth="1"
                      strokeOpacity="0.45"
                      className="increase-highlight-circle"
                    />
                  )}

                  {/* Invisible hit area for easier clicking */}
                  <circle cx="0" cy="0" r="14" fill="transparent" />

                  {/* Render standard CYC vector symbol */}
                  <RenderStitchSymbol
                    stitchType={node.stitch_type}
                    symbolName={node.symbol_name}
                    color={color}
                    size={22}
                    isSelected={isSelected}
                    isHovered={isHovered}
                    isActiveStep={isActivePlaybackNode}
                  />

                  {/* Optional Stitch Index Number */}
                  {showNumbers && (
                    <text
                      x="0"
                      y="-12"
                      fontSize="8"
                      textAnchor="middle"
                      fill="var(--text-muted)"
                      transform={`rotate(${-node.rotation})`}
                      className="stitch-index-label"
                    >
                      {node.stitch_index}
                    </text>
                  )}
                </g>
              );
            })}
          </g>
        </g>
      </svg>

      {/* Stitch Inspector Tooltip on Hover / Selection */}
      {(hoveredNode || selectedNode) && (
        <div className="stitch-inspector-card">
          {(() => {
            const n = hoveredNode || selectedNode!;
            return (
              <>
                <div className="inspector-header">
                  <span className="badge-round">R{n.unit_index || n.unit_number || 1}</span>
                  <span className="badge-stitch">#{n.stitch_index}</span>
                  <span className="badge-type">{n.stitch_type.toUpperCase()}</span>
                </div>
                <div className="inspector-details">
                  <div className="inspector-row">
                    <span className="label">Symbol:</span>
                    <span className="val">{n.symbol_name}</span>
                  </div>
                  <div className="inspector-row">
                    <span className="label">Position:</span>
                    <span className="val">({Math.round(n.x)}, {Math.round(n.y)})</span>
                  </div>
                  <div className="inspector-row">
                    <span className="label">Rotation:</span>
                    <span className="val">{Math.round(n.rotation)}°</span>
                  </div>
                </div>
              </>
            );
          })()}
        </div>
      )}

      {/* Empty State when no chart loaded */}
      {!chart && (
        <div className="canvas-empty-state">
          <div className="empty-icon-wrap">
            <Info size={40} />
          </div>
          <h3>No Pattern Chart Loaded</h3>
          <p>Type or paste a crochet pattern on the left, or pick a sample preset to generate a vector chart.</p>
        </div>
      )}
    </div>
  );
};
