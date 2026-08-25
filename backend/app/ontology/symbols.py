"""
Standard Crochet Symbol Vector Definitions (Craft Yarn Council Standard).
Provides SVG paths, dimensions, viewboxes, and drawing helpers for chart rendering.
"""

from typing import Dict, Any

# Standard symbol definitions with SVG path data
CYC_SYMBOLS: Dict[str, Dict[str, Any]] = {
    "chain_oval": {
        "name": "Chain (ch)",
        "viewBox": "-15 -8 30 16",
        "svg": '<ellipse cx="0" cy="0" rx="12" ry="6" fill="none" stroke="currentColor" stroke-width="2.5" />',
        "width": 24,
        "height": 12,
    },
    "slip_stitch_dot": {
        "name": "Slip Stitch (sl st)",
        "viewBox": "-8 -8 16 16",
        "svg": '<circle cx="0" cy="0" r="5" fill="currentColor" />',
        "width": 10,
        "height": 10,
    },
    "sc_plus": {
        "name": "Single Crochet (sc / + / x)",
        "viewBox": "-12 -12 24 24",
        "svg": '<line x1="-8" y1="0" x2="8" y2="0" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><line x1="0" y1="-8" x2="0" y2="8" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>',
        "width": 16,
        "height": 16,
    },
    "hdc_tee": {
        "name": "Half Double Crochet (hdc / T)",
        "viewBox": "-12 -18 24 36",
        "svg": '<line x1="0" y1="-14" x2="0" y2="14" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><line x1="-8" y1="-14" x2="8" y2="-14" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>',
        "width": 16,
        "height": 28,
    },
    "dc_cross": {
        "name": "Double Crochet (dc)",
        "viewBox": "-12 -22 24 44",
        "svg": '<line x1="0" y1="-18" x2="0" y2="18" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><line x1="-8" y1="-18" x2="8" y2="-18" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><line x1="-6" y1="0" x2="6" y2="-4" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>',
        "width": 16,
        "height": 36,
    },
    "tr_double_cross": {
        "name": "Treble Crochet (tr)",
        "viewBox": "-12 -26 24 52",
        "svg": '<line x1="0" y1="-22" x2="0" y2="22" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><line x1="-8" y1="-22" x2="8" y2="-22" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><line x1="-6" y1="-6" x2="6" y2="-10" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><line x1="-6" y1="6" x2="6" y2="2" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>',
        "width": 16,
        "height": 44,
    },
    "dtr_triple_cross": {
        "name": "Double Treble Crochet (dtr)",
        "viewBox": "-12 -30 24 60",
        "svg": '<line x1="0" y1="-26" x2="0" y2="26" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><line x1="-8" y1="-26" x2="8" y2="-26" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><line x1="-6" y1="-12" x2="6" y2="-16" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><line x1="-6" y1="0" x2="6" y2="-4" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><line x1="-6" y1="12" x2="6" y2="8" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>',
        "width": 16,
        "height": 52,
    },
    "magic_ring_loop": {
        "name": "Magic Ring (MR)",
        "viewBox": "-18 -18 36 36",
        "svg": '<circle cx="0" cy="0" r="12" fill="none" stroke="currentColor" stroke-width="2.5" stroke-dasharray="3 3"/><circle cx="0" cy="0" r="3" fill="currentColor" />',
        "width": 24,
        "height": 24,
    },
    "sc_inc_v": {
        "name": "Single Crochet Increase (2 sc in 1)",
        "viewBox": "-16 -16 32 32",
        "svg": '<path d="M -10 -10 L 0 12 L 10 -10" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/><line x1="-12" y1="-6" x2="-4" y2="-6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><line x1="4" y1="-6" x2="12" y2="-6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
        "width": 24,
        "height": 24,
    },
    "dc_inc_v": {
        "name": "Double Crochet Increase (2 dc in 1)",
        "viewBox": "-18 -22 36 44",
        "svg": '<path d="M -12 -18 L 0 18 L 12 -18" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/><line x1="-16" y1="-18" x2="-8" y2="-18" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><line x1="8" y1="-18" x2="16" y2="-18" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><line x1="-11" y1="-2" x2="-3" y2="-6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><line x1="3" y1="-6" x2="11" y2="-2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
        "width": 28,
        "height": 36,
    },
    "sc_dec_inv_v": {
        "name": "Single Crochet Decrease (sc2tog)",
        "viewBox": "-16 -16 32 32",
        "svg": '<path d="M -10 12 L 0 -10 L 10 12" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/><line x1="-7" y1="2" x2="7" y2="2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
        "width": 24,
        "height": 24,
    },
    "dc_dec_inv_v": {
        "name": "Double Crochet Decrease (dc2tog)",
        "viewBox": "-18 -22 36 44",
        "svg": '<path d="M -12 18 L 0 -18 L 12 18" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/><line x1="-6" y1="-18" x2="6" y2="-18" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><line x1="-10" y1="2" x2="-3" y2="-2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><line x1="3" y1="-2" x2="10" y2="2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
        "width": 28,
        "height": 36,
    },
    "puff_oval": {
        "name": "Puff / Bobble Stitch",
        "viewBox": "-14 -18 28 36",
        "svg": '<ellipse cx="0" cy="0" rx="9" ry="14" fill="none" stroke="currentColor" stroke-width="2.2"/><line x1="0" y1="-14" x2="0" y2="14" stroke="currentColor" stroke-width="1.8" stroke-dasharray="2 2"/><line x1="-6" y1="-14" x2="6" y2="-14" stroke="currentColor" stroke-width="2.5"/>',
        "width": 20,
        "height": 28,
    },
    "popcorn_cluster": {
        "name": "Popcorn Stitch",
        "viewBox": "-16 -18 32 36",
        "svg": '<ellipse cx="0" cy="0" rx="12" ry="14" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M -8 -8 C -4 -16 4 -16 8 -8" fill="none" stroke="currentColor" stroke-width="2"/>',
        "width": 24,
        "height": 28,
    },
    "picot_triangle": {
        "name": "Picot Stitch",
        "viewBox": "-12 -14 24 28",
        "svg": '<circle cx="-6" cy="-4" r="3.5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="0" cy="-10" r="3.5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="6" cy="-4" r="3.5" fill="none" stroke="currentColor" stroke-width="1.8"/>',
        "width": 20,
        "height": 20,
    },
    "skip_dash": {
        "name": "Skip Stitch",
        "viewBox": "-10 -6 20 12",
        "svg": '<line x1="-7" y1="0" x2="7" y2="0" stroke="currentColor" stroke-width="2.5" stroke-dasharray="3 3"/>',
        "width": 14,
        "height": 6,
    }
}
