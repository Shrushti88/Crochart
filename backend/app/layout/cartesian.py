"""
Cartesian Layout Engine for Row-Based Crochet Patterns.
Calculates 2D horizontal/vertical coordinates, alternating directions (turn work), and links.
"""

from typing import List, Dict, Tuple
from ..ontology.schema import (
    CrochetPatternAST, StitchInstruction, RepeatGroup,
    StitchType, ChartNode, ChartLink, UnitType
)
from ..ontology.vocabulary import STITCH_METADATA

class CartesianLayoutEngine:
    ROW_COLORS = [
        "#2563EB", # Blue
        "#DB2777", # Pink
        "#059669", # Green
        "#7C3AED", # Violet
        "#D97706", # Amber
        "#0891B2", # Cyan
        "#DC2626", # Red
        "#4F46E5", # Indigo
    ]

    @classmethod
    def generate(cls, ast: CrochetPatternAST) -> Tuple[List[ChartNode], List[ChartLink], Dict[str, float]]:
        nodes: List[ChartNode] = []
        links: List[ChartLink] = []
        
        spacing_x = 28.0
        base_y = 0.0
        prev_row_node_ids: List[str] = []

        for u_idx, unit in enumerate(ast.units):
            flat_stitches = cls._flatten_instructions(unit.instructions)
            total_st = len(flat_stitches)
            if total_st == 0:
                continue

            current_row_node_ids: List[str] = []
            color = cls.ROW_COLORS[u_idx % len(cls.ROW_COLORS)]
            
            # Determine direction: Row 1 = L to R, Row 2 = R to L, etc.
            # (or if unit index is even, go right-to-left)
            is_reverse = (unit.index % 2 == 0)

            # Check height of row
            max_height = 1.0
            for st in flat_stitches:
                meta = STITCH_METADATA.get(st.stitch_type, {})
                h = meta.get("height_units", 1.0)
                if h > max_height:
                    max_height = h
                    
            row_y = base_y - (u_idx * 40.0 * max_height)

            for s_idx, st in enumerate(flat_stitches):
                node_id = f"node_row{unit.index}_s{s_idx + 1}"
                
                # Compute X position based on direction
                col = (total_st - 1 - s_idx) if is_reverse else s_idx
                x = col * spacing_x
                y = row_y

                meta = STITCH_METADATA.get(st.stitch_type, {})
                symbol = meta.get("symbol", "sc_plus")
                
                parent_ids = []
                if prev_row_node_ids:
                    # Link to stitch below
                    p_idx = int((s_idx / total_st) * len(prev_row_node_ids))
                    p_idx = min(p_idx, len(prev_row_node_ids) - 1)
                    parent_ids = [prev_row_node_ids[p_idx]]

                node = ChartNode(
                    id=node_id,
                    unit_type=UnitType.ROW,
                    unit_index=unit.index,
                    stitch_index=s_idx + 1,
                    stitch_type=st.stitch_type,
                    symbol_name=symbol,
                    x=round(x, 2),
                    y=round(y, 2),
                    rotation=0.0,
                    target_loop=st.target_loop,
                    color=color,
                    label=f"R{unit.index}:{s_idx + 1}",
                    parent_ids=parent_ids,
                    line_number=st.line_number
                )
                nodes.append(node)
                current_row_node_ids.append(node_id)

                for pid in parent_ids:
                    links.append(ChartLink(
                        id=f"link_{pid}_{node_id}",
                        source_id=pid,
                        target_id=node_id,
                        link_type="base"
                    ))

            prev_row_node_ids = current_row_node_ids

        bounds = cls._calc_bounds(nodes)
        return nodes, links, bounds

    @classmethod
    def _flatten_instructions(cls, instructions: List) -> List[StitchInstruction]:
        flat: List[StitchInstruction] = []
        for inst in instructions:
            if isinstance(inst, RepeatGroup):
                sub_flat = cls._flatten_instructions(inst.instructions)
                for _ in range(inst.repeat_count):
                    flat.extend(sub_flat)
            elif isinstance(inst, StitchInstruction):
                if inst.count > 1 and inst.stitch_type in (StitchType.SC, StitchType.DC, StitchType.HDC, StitchType.TR, StitchType.CH, StitchType.SL_ST):
                    for _ in range(inst.count):
                        flat.append(StitchInstruction(
                            id=inst.id,
                            stitch_type=inst.stitch_type,
                            count=1,
                            target_loop=inst.target_loop,
                            in_same_stitch=inst.in_same_stitch,
                            target_stitch_count=1,
                            produced_stitch_count=1,
                            raw_text=inst.raw_text,
                            line_number=inst.line_number
                        ))
                else:
                    flat.append(inst)
        return flat

    @classmethod
    def _calc_bounds(cls, nodes: List[ChartNode]) -> Dict[str, float]:
        if not nodes:
            return {"min_x": 0, "max_x": 300, "min_y": -200, "max_y": 50, "width": 300, "height": 250}
        
        min_x = min(n.x for n in nodes) - 30
        max_x = max(n.x for n in nodes) + 30
        min_y = min(n.y for n in nodes) - 30
        max_y = max(n.y for n in nodes) + 30
        
        return {
            "min_x": round(min_x, 1),
            "max_x": round(max_x, 1),
            "min_y": round(min_y, 1),
            "max_y": round(max_y, 1),
            "width": round(max_x - min_x, 1),
            "height": round(max_y - min_y, 1),
        }
