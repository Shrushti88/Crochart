import pytest
from app.samples.sample_library import SAMPLE_PATTERNS
from app.parser.ast_parser import ASTParser
from app.layout.graph_builder import ChartGraphBuilder
from app.validator.rules import PatternValidator

def test_all_sample_patterns_parse_and_render():
    assert len(SAMPLE_PATTERNS) >= 20
    parser = ASTParser()
    
    for sample in SAMPLE_PATTERNS:
        raw = sample["pattern"]
        title = sample["title"]
        ast = parser.parse(raw, title=title)
        
        # Verify AST has units
        assert len(ast.units) > 0, f"Sample '{title}' produced 0 AST units"
        
        # Verify Validation runs
        report = PatternValidator.validate(ast)
        assert report is not None
        
        # Verify Chart Graph is built
        graph = ChartGraphBuilder.build(ast)
        assert graph.total_stitches > 0, f"Sample '{title}' produced 0 stitches in graph"
        assert len(graph.nodes) > 0
        assert graph.bounds["width"] > 0
