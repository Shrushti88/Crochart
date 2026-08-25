export type StitchType =
  | "ch"
  | "sl_st"
  | "sc"
  | "hdc"
  | "dc"
  | "tr"
  | "dtr"
  | "inc"
  | "dec"
  | "sc2tog"
  | "sc3tog"
  | "dc2tog"
  | "dc3tog"
  | "cluster"
  | "popcorn"
  | "puff"
  | "bobble"
  | "magic_ring"
  | "picot"
  | "custom";

export type UnitType = "round" | "row" | "motif";
export type TerminologyStandard = "US" | "UK";

export interface StitchInstructionAST {
  id: string;
  stitch_type: StitchType;
  count: number;
  target_loop?: string;
  in_same_stitch?: boolean;
  target_stitch_count?: number;
  produced_stitch_count?: number;
  chain_space_size?: number;
  raw_text?: string;
  line_number?: number;
}

export interface RepeatGroupAST {
  id: string;
  instructions: (StitchInstructionAST | RepeatGroupAST)[];
  repeat_count: number;
  raw_text?: string;
  line_number?: number;
}

export interface PatternUnitAST {
  unit_type: UnitType;
  index: number;
  raw_header?: string;
  raw_text?: string;
  instructions: (StitchInstructionAST | RepeatGroupAST)[];
  stated_stitch_count?: number;
  computed_produced_count?: number;
  computed_consumed_count?: number;
  is_joined?: boolean;
  is_turned?: boolean;
  line_number?: number;
}

export interface CrochetPatternAST {
  title: string;
  terminology: TerminologyStandard;
  is_circular: boolean;
  units: PatternUnitAST[];
  total_units?: number;
  raw_text?: string;
  metadata?: Record<string, any>;
}

export interface Diagnostic {
  severity: "error" | "warning" | "info";
  rule_code: string;
  message: string;
  unit_index?: number;
  unit_number?: number;
  line_number?: number;
  suggested_fix?: string;
  suggestion?: string;
  expected_value?: number;
  actual_value?: number;
}

export interface ValidationReport {
  is_valid: boolean;
  total_diagnostics?: number;
  errors_count?: number;
  warnings_count?: number;
  error_count?: number;
  warning_count?: number;
  diagnostics?: Diagnostic[];
  issues?: Diagnostic[];
  summary?: string;
  unit_stitch_counts?: Record<string, number>;
  expected_vs_actual?: Record<string, { expected: number; actual: number }>;
}

export interface ChartNode {
  id: string;
  unit_type?: string;
  unit_index: number;
  unit_number?: number;
  stitch_index: number;
  stitch_type: StitchType;
  symbol_name: string;
  x: number;
  y: number;
  rotation: number;
  color?: string;
  label?: string;
  tooltip?: string;
  parent_ids?: string[];
  line_number?: number;
}

export interface ChartLink {
  id?: string;
  source_id: string;
  target_id: string;
  link_type: string;
}

export interface ChartBounds {
  min_x: number;
  max_x: number;
  min_y: number;
  max_y: number;
  width: number;
  height: number;
}

export interface ChartGraph {
  pattern_title: string;
  is_circular: boolean;
  units_count: number;
  total_stitches: number;
  nodes: ChartNode[];
  links: ChartLink[];
  bounds: ChartBounds;
  legend?: Array<{ symbol_name: string; label: string; count: number }>;
  center?: [number, number];
  round_radii?: Record<number, number>;
  metadata?: Record<string, any>;
}

export interface ParseResponse {
  ast: CrochetPatternAST;
  validation: ValidationReport;
}

export interface SamplePattern {
  id: string;
  title: string;
  category: "amigurumi" | "flat_motif" | "mandala" | "row_fabric" | "flower" | string;
  difficulty: "beginner" | "intermediate" | "advanced" | string;
  description: string;
  terminology: TerminologyStandard;
  is_circular: boolean;
  pattern_text: string;
  tags: string[];
  color_theme?: string[];
}

export interface DBProject {
  id: number;
  title: string;
  description: string;
  raw_pattern: string;
  terminology: string;
  is_circular: boolean;
  ast_data?: CrochetPatternAST;
  chart_data?: ChartGraph;
}
