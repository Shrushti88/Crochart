import pytest
from app.parser.preprocessor import Preprocessor
from app.parser.tokenizer import PatternTokenizer
from app.parser.ast_parser import ASTParser
from app.ontology.schema import StitchType, UnitType, LoopTarget, TerminologyStandard

def test_preprocessor_abbreviations():
    text = "R1: mr, 6sc, 2sc in next st, sc2tog, inv dec"
    cleaned = Preprocessor.standardize_abbreviations(text)
    assert "magic ring" in cleaned
    assert "inc" in cleaned
    assert "dec" in cleaned

def test_preprocessor_uk_translation():
    text = "Round 1: 6 dc in magic ring"
    translated = Preprocessor.normalize_terms(text, source_term=TerminologyStandard.UK, target_term=TerminologyStandard.US)
    assert "6 sc" in translated

def test_tokenizer_header_and_count():
    line = "Round 2: [sc, inc] * 6 (18 sts)"
    unit_type, unit_index, stated_count, body = PatternTokenizer.extract_header_and_count(line, 1)
    assert unit_type == UnitType.ROUND
    assert unit_index == 2
    assert stated_count == 18
    assert "[sc, inc] * 6" in body

def test_ast_parser_magic_ring():
    pattern = "Round 1: Magic ring, 6 sc (6)"
    parser = ASTParser()
    ast = parser.parse(pattern)
    assert len(ast.units) == 1
    assert ast.units[0].stated_stitch_count == 6
    assert ast.units[0].computed_produced_count == 6

def test_ast_parser_bracket_repeats():
    pattern = """Round 1: Magic ring, 6 sc (6)
Round 2: [inc] * 6 (12)
Round 3: [sc, inc] * 6 (18)"""
    parser = ASTParser()
    ast = parser.parse(pattern)
    assert len(ast.units) == 3
    assert ast.units[1].computed_produced_count == 12
    assert ast.units[2].computed_produced_count == 18

def test_ast_parser_nested_repeats():
    pattern = "Row 1: Ch 20 (20)\nRow 2: [2 sc, [inc, sc] * 2] * 2 (16)"
    parser = ASTParser()
    ast = parser.parse(pattern)
    assert len(ast.units) == 2
    assert not ast.is_circular
