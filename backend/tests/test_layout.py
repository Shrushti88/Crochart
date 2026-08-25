import pytest
from app.parser.ast_parser import ASTParser
from app.layout.graph_builder import ChartGraphBuilder
from app.ontology.schema import UnitType

def test_radial_layout_generation():
    pattern = """Round 1: Magic ring, 6 sc (6)
Round 2: [inc] * 6 (12)"""
    parser = ASTParser()
    ast = parser.parse(pattern)
    graph = ChartGraphBuilder.build(ast)
    assert graph.is_circular
    # 1 MR node + 6 round 1 nodes + 6 increase nodes in round 2 = 13 nodes
    assert graph.total_stitches >= 12
    assert len(graph.links) > 0
    assert graph.bounds["width"] > 0

def test_cartesian_layout_generation():
    pattern = """Row 1: Ch 10, turn (10)
Row 2: 9 sc, turn (9)
Row 3: 9 sc, turn (9)"""
    parser = ASTParser()
    ast = parser.parse(pattern)
    graph = ChartGraphBuilder.build(ast)
    assert not graph.is_circular
    assert graph.total_stitches >= 20
    assert len(graph.links) > 0
