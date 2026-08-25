import React from 'react';
import { StitchType } from '../../types';

interface SymbolProps {
  stitchType: StitchType | string;
  symbolName?: string;
  color?: string;
  size?: number;
  isSelected?: boolean;
  isHovered?: boolean;
  isActiveStep?: boolean;
}

export const CYC_SYMBOL_DEFS: Record<string, { label: string; description: string; abbrev: string }> = {
  ch: { label: 'Chain', description: 'Open oval loop', abbrev: 'ch' },
  sl_st: { label: 'Slip Stitch', description: 'Solid dot / filled crescent', abbrev: 'sl st' },
  sc: { label: 'Single Crochet', description: 'Cross / Plus symbol (+)', abbrev: 'sc' },
  hdc: { label: 'Half Double Crochet', description: 'T-bar symbol', abbrev: 'hdc' },
  dc: { label: 'Double Crochet', description: 'T-bar with 1 cross-hatch', abbrev: 'dc' },
  tr: { label: 'Treble Crochet', description: 'T-bar with 2 cross-hatches', abbrev: 'tr' },
  dtr: { label: 'Double Treble', description: 'T-bar with 3 cross-hatches', abbrev: 'dtr' },
  inc: { label: 'Increase (2 in 1)', description: 'V-branching stitch', abbrev: 'inc' },
  dec: { label: 'Decrease (2tog)', description: 'Inverted V joined at top', abbrev: 'dec' },
  sc2tog: { label: 'Single Crochet 2 Together', description: '2 sc converging at top', abbrev: 'sc2tog' },
  dc2tog: { label: 'Double Crochet 2 Together', description: '2 dc converging at top', abbrev: 'dc2tog' },
  cluster: { label: 'Cluster / Puff', description: 'Multiple stitches in 1 space joined at top', abbrev: 'cl' },
  magic_ring: { label: 'Magic Ring', description: 'Adjustable foundation loop', abbrev: 'MR' },
  picot: { label: 'Picot (ch 3, sl st)', description: 'Pointed chain loop', abbrev: 'picot' },
};

export const RenderStitchSymbol: React.FC<SymbolProps> = ({
  stitchType,
  symbolName,
  color = 'currentColor',
  size = 20,
  isSelected,
  isHovered,
  isActiveStep
}) => {
  const type = (symbolName || stitchType).toLowerCase();

  const strokeColor = color;
  const fillColor = color;
  const strokeWidth = isSelected || isActiveStep ? 2.5 : isHovered ? 2.2 : 1.8;

  let content: React.ReactNode;

  if (type.includes('ch_oval') || type === 'ch') {
    content = (
      <ellipse
        cx="0"
        cy="0"
        rx="5.5"
        ry="3"
        fill={isSelected ? `${color}33` : 'none'}
        stroke={strokeColor}
        strokeWidth={strokeWidth}
      />
    );
  } else if (type.includes('sl_st') || type === 'sl st') {
    content = (
      <circle
        cx="0"
        cy="0"
        r="3.5"
        fill={fillColor}
      />
    );
  } else if (type.includes('sc_plus') || type.includes('sc_cross') || type === 'sc' || type === 'single') {
    content = (
      <g>
        <line x1="-4.5" y1="-4.5" x2="4.5" y2="4.5" stroke={strokeColor} strokeWidth={strokeWidth} strokeLinecap="round" />
        <line x1="-4.5" y1="4.5" x2="4.5" y2="-4.5" stroke={strokeColor} strokeWidth={strokeWidth} strokeLinecap="round" />
      </g>
    );
  } else if (type.includes('hdc_t') || type === 'hdc') {
    content = (
      <g>
        <line x1="0" y1="-7" x2="0" y2="7" stroke={strokeColor} strokeWidth={strokeWidth} strokeLinecap="round" />
        <line x1="-6" y1="-7" x2="6" y2="-7" stroke={strokeColor} strokeWidth={strokeWidth} strokeLinecap="round" />
      </g>
    );
  } else if (type.includes('dc_cross') || type === 'dc') {
    content = (
      <g>
        <line x1="0" y1="-9" x2="0" y2="9" stroke={strokeColor} strokeWidth={strokeWidth} strokeLinecap="round" />
        <line x1="-6" y1="-9" x2="6" y2="-9" stroke={strokeColor} strokeWidth={strokeWidth} strokeLinecap="round" />
        <line x1="-3.5" y1="0" x2="3.5" y2="-2.5" stroke={strokeColor} strokeWidth={strokeWidth} strokeLinecap="round" />
      </g>
    );
  } else if (type.includes('tr_cross') || type === 'tr') {
    content = (
      <g>
        <line x1="0" y1="-12" x2="0" y2="12" stroke={strokeColor} strokeWidth={strokeWidth} strokeLinecap="round" />
        <line x1="-6" y1="-12" x2="6" y2="-12" stroke={strokeColor} strokeWidth={strokeWidth} strokeLinecap="round" />
        <line x1="-3.5" y1="-3" x2="3.5" y2="-5" stroke={strokeColor} strokeWidth={strokeWidth} strokeLinecap="round" />
        <line x1="-3.5" y1="3" x2="3.5" y2="1" stroke={strokeColor} strokeWidth={strokeWidth} strokeLinecap="round" />
      </g>
    );
  } else if (type.includes('inc_v') || type === 'inc') {
    content = (
      <g>
        <path d="M-5.5 -7 L0 6.5 L5.5 -7" fill="none" stroke={strokeColor} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" />
        <line x1="-4.5" y1="-2.5" x2="-1.5" y2="-2.5" stroke={strokeColor} strokeWidth={strokeWidth - 0.2} strokeLinecap="round" />
        <line x1="1.5" y1="-2.5" x2="4.5" y2="-2.5" stroke={strokeColor} strokeWidth={strokeWidth - 0.2} strokeLinecap="round" />
      </g>
    );
  } else if (type.includes('dec_inv_v') || type === 'dec' || type.includes('2tog')) {
    content = (
      <g>
        <path d="M-6 7 L0 -7 L6 7" fill="none" stroke={strokeColor} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" />
        <line x1="-5" y1="3" x2="-2" y2="3" stroke={strokeColor} strokeWidth={strokeWidth - 0.2} strokeLinecap="round" />
        <line x1="2" y1="3" x2="5" y2="3" stroke={strokeColor} strokeWidth={strokeWidth - 0.2} strokeLinecap="round" />
      </g>
    );
  } else if (type.includes('magic_ring') || type === 'magic_ring') {
    content = (
      <g>
        <circle cx="0" cy="0" r="7" fill="none" stroke={strokeColor} strokeWidth={strokeWidth} strokeDasharray="3 2" />
        <circle cx="0" cy="0" r="3" fill={fillColor} />
      </g>
    );
  } else if (type.includes('picot')) {
    content = (
      <g>
        <circle cx="-3" cy="-4" r="2.5" fill="none" stroke={strokeColor} strokeWidth={strokeWidth - 0.4} />
        <circle cx="0" cy="-7" r="2.5" fill="none" stroke={strokeColor} strokeWidth={strokeWidth - 0.4} />
        <circle cx="3" cy="-4" r="2.5" fill="none" stroke={strokeColor} strokeWidth={strokeWidth - 0.4} />
      </g>
    );
  } else if (type.includes('cluster') || type.includes('puff') || type.includes('popcorn')) {
    content = (
      <g>
        <path d="M-6 8 C-7 0, -5 -7, 0 -9 C5 -7, 7 0, 6 8 Z" fill={isSelected ? `${color}33` : 'none'} stroke={strokeColor} strokeWidth={strokeWidth} strokeLinejoin="round" />
        <line x1="0" y1="-9" x2="0" y2="8" stroke={strokeColor} strokeWidth={strokeWidth - 0.5} strokeDasharray="2 2" />
      </g>
    );
  } else {
    // Default circle node
    content = (
      <circle
        cx="0"
        cy="0"
        r="4.5"
        fill={isSelected ? fillColor : 'none'}
        stroke={strokeColor}
        strokeWidth={strokeWidth}
      />
    );
  }

  return (
    <g className="cyc-symbol-glyph">
      {(isSelected || isActiveStep) && (
        <circle
          cx="0"
          cy="0"
          r={size / 1.3}
          fill="none"
          stroke={color}
          strokeWidth="2"
          strokeDasharray="4 3"
          className="pulse-halo"
          opacity="0.8"
        />
      )}
      {content}
    </g>
  );
};
