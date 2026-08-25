"""
Radial (Circular) Layout Engine for Crochet in the Round.
Calculates 2D polar/radial coordinates, angles, and parent stitch linkages for rounds.
"""

import math
from typing import List, Dict, Tuple, Optional
from ..ontology.schema import (
    CrochetPatternAST, PatternUnit, StitchInstruction, RepeatGroup,
    StitchType, ChartNode, ChartLink, UnitType
)
from ..ontology.vocabulary import STITCH_METADATA

class RadialLayoutEngine:
    # Color palette for distinct rounds
    ROUND_COLORS = [
        "#3B82F6", # Blue
        "#EC4899", # Pink
        "#10B981", # Emerald
        "#8B5CF6", # Violet
        "#F59E0B", # Amber
        "#06B6D4", # Cyan
        "#EF4444", # Red
        "#6366F1", # Indigo
        "#14B8A6", # Teal
        "#F97316", # Orange
    ]

    @classmethod
    def generate(cls, ast: CrochetPatternAST) -> Tuple[List[ChartNode], List[ChartLink], Dict[str, float]]:
        nodes: List[ChartNode] = []
        links: List[ChartLink] = []
        
        # Track stitches produced in previous round to create link connections
        prev_round_node_ids: List[str] = []
        
        base_radius = 40.0
        radius_step = 30.0
        
        # Center Magic Ring node if starting with MR
        first_unit = ast.units[0] if ast.units else None
        has_mr = False
        if first_unit:
            for inst in first_unit.instructions:
                if isinstance(inst, StitchInstruction) and inst.stitch_type == StitchType.MAGIC_RING:
                    has_mr = True
                    break
                    
        if has_mr:
            mr_id = "node_mr_0"
            nodes.append(ChartNode(
                id=mr_id,
                unit_type=UnitType.ROUND,
                unit_index=0,
                stitch_index=0,
                stitch_type=StitchType.MAGIC_RING,
                symbol_name="magic_ring_loop",
                x=0.0,
                y=0.0,
                rotation=0.0,
                color="#8B5CF6",
                label="MR",
                line_number=first_unit.line_number
            ))
            prev_round_node_ids = [mr_id]
            
        current_radius = base_radius

        for u_idx, unit in enumerate(ast.units):
            # Flatten unit instructions into individual stitch tokens
            flat_stitches = cls._flatten_instructions(unit.instructions)
            total_st_in_unit = len(flat_stitches)
            if total_st_in_unit == 0:
                continue

            current_round_node_ids: List[str] = []
            color = cls.ROUND_COLORS[u_idx % len(cls.ROUND_COLORS)]
            angle_step = (2 * math.pi) / max(total_st_in_unit, 1)

            # Check max stitch height in this unit to adjust radius spacing
            max_height = 1.0
            for st in flat_stitches:
                meta = STITCH_METADATA.get(st.stitch_type, {})
                h = meta.get("height_units", 1.0)
                if h > max_height:
                    max_height = h
            current_radius += (max_height * 12.0)

            for s_idx, st in enumerate(flat_stitches):
                node_id = f"node_r{unit.index}_s{s_idx + 1}"
                angle = (s_idx * angle_step) - (math.pi / 2) # Start top at -90 deg
                
                # Cartesian coordinates from polar
                x = current_radius * math.cos(angle)
                y = current_radius * math.sin(angle)
                
                # Rotation so symbol points radially outward
                deg = math.degrees(angle) + 90.0
                
                meta = STITCH_METADATA.get(st.stitch_type, {})
                symbol = meta.get("symbol", "sc_plus")
                
                parent_ids = []
                if prev_round_node_ids:
                    if len(prev_round_node_ids) == 1 and prev_round_node_ids[0] == "node_mr_0":
                        parent_ids = ["node_mr_0"]
                    else:
                        # Map fractionally to parent round stitch
                        p_idx = int((s_idx / total_st_in_unit) * len(prev_round_node_ids))
                        p_idx = min(p_idx, len(prev_round_node_ids) - 1)
                        parent_ids = [prev_round_node_ids[p_idx]]

                # Create Node
                node = ChartNode(
                    id=node_id,
                    unit_type=UnitType.ROUND,
                    unit_index=unit.index,
                    stitch_index=s_idx + 1,
                    stitch_type=st.stitch_type,
                    symbol_name=symbol,
                    x=round(x, 2),
                    y=round(y, 2),
                    rotation=round(deg, 1),
                    target_loop=st.target_loop,
                    color=color,
                    label=f"R{unit.index}:{s_idx + 1}",
                    parent_ids=parent_ids,
                    line_number=st.line_number
                )
                nodes.append(node)
                current_round_node_ids.append(node_id)

                # Create link from parent
                for pid in parent_ids:
                    links.append(ChartLink(
                        id=f"link_{pid}_{node_id}",
                        source_id=pid,
                        target_id=node_id,
                        link_type="base"
                    ))

            # Connect join slip-stitch if round is joined
            if unit.is_joined and len(current_round_node_ids) > 1:
                links.append(ChartLink(
                    id=f"link_join_r{unit.index}",
                    source_id=current_round_node_ids[-1],
                    target_id=current_round_node_ids[0],
                    link_type="join"
                ))

            prev_round_node_ids = current_round_node_ids
            current_radius += radius_step

        # Calculate bounding box
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
                if inst.stitch_type == StitchType.MAGIC_RING:
                    continue
                # For instructions with count > 1 (e.g. 6 sc), expand to individual stitch nodes
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
            return {"min_x": -100, "max_x": 100, "min_y": -100, "max_y": 100, "width": 200, "height": 200}
        
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
