import pytest
from app.parser.ast_parser import ASTParser
from app.validator.rules import PatternValidator
from app.validator.diagnostics import DiagnosticSeverity

def test_validator_perfect_pattern():
    pattern = """Round 1: Magic ring, 6 sc (6)
Round 2: [inc] * 6 (12)
Round 3: [sc, inc] * 6 (18)"""
    parser = ASTParser()
    ast = parser.parse(pattern)
    report = PatternValidator.validate(ast)
    assert report.is_valid
    assert report.errors_count == 0
    assert report.warnings_count == 0

def test_validator_stated_count_mismatch():
    # Stated 20 instead of 18
    pattern = """Round 1: Magic ring, 6 sc (6)
Round 2: [inc] * 6 (12)
Round 3: [sc, inc] * 6 (20)"""
    parser = ASTParser()
    ast = parser.parse(pattern)
    report = PatternValidator.validate(ast)
    assert report.total_diagnostics > 0
    codes = [d.rule_code for d in report.diagnostics]
    assert "STATED_COUNT_MISMATCH" in codes

def test_validator_conservation_mismatch():
    # Round 2 consumes 12 stitches from Round 1, but Round 1 only produced 6
    pattern = """Round 1: Magic ring, 6 sc (6)
Round 2: [inc] * 12 (24)"""
    parser = ASTParser()
    ast = parser.parse(pattern)
    report = PatternValidator.validate(ast)
    codes = [d.rule_code for d in report.diagnostics]
    assert "CONSERVATION_MISMATCH" in codes
