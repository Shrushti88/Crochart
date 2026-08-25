"""
High-level Chart Graph Builder.
Selects Radial or Cartesian layout engine and produces comprehensive ChartGraph with legend.
"""

from typing import List, Dict, Set
from ..ontology.schema import CrochetPatternAST, ChartGraph, StitchType
from ..ontology.vocabulary import STITCH_METADATA
from .radial import RadialLayoutEngine
from .cartesian import CartesianLayoutEngine

class ChartGraphBuilder:
    @classmethod
    def build(cls, ast: CrochetPatternAST) -> ChartGraph:
        if ast.is_circular:
            nodes, links, bounds = RadialLayoutEngine.generate(ast)
        else:
            nodes, links, bounds = CartesianLayoutEngine.generate(ast)

        # Build legend of symbols used in this chart
        used_stitch_types: Set[StitchType] = {node.stitch_type for node in nodes}
        legend: List[Dict[str, str]] = []
        
        for st in used_stitch_types:
            meta = STITCH_METADATA.get(st, {})
            legend.append({
                "stitch_type": st.value,
                "name": meta.get("name", st.value),
                "symbol_name": meta.get("symbol", "sc_plus"),
                "abbr": meta.get("us_abbr", st.value),
                "category": meta.get("category", "basic"),
            })

        return ChartGraph(
            pattern_title=ast.title,
            is_circular=ast.is_circular,
            nodes=nodes,
            links=links,
            bounds=bounds,
            total_stitches=len(nodes),
            units_count=len(ast.units),
            legend=legend
        )
