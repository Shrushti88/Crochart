"""
Crochet Pattern Validation Rules Engine.
Detects stitch count mismatches, missing rounds, impossible stitch operations, and syntax anomalies.
"""

from typing import List
from ..ontology.schema import CrochetPatternAST, PatternUnit, UnitType, StitchType, StitchInstruction, RepeatGroup
from .diagnostics import ValidationReport, Diagnostic, DiagnosticSeverity

class PatternValidator:
    @classmethod
    def validate(cls, ast: CrochetPatternAST) -> ValidationReport:
        diagnostics: List[Diagnostic] = []

        if not ast.units:
            diagnostics.append(Diagnostic(
                line_number=1,
                severity=DiagnosticSeverity.ERROR,
                rule_code="EMPTY_PATTERN",
                message="Pattern has no readable rounds or rows.",
                suggested_fix="Enter at least one Round or Row instruction (e.g. 'Round 1: Magic ring, 6 sc')."
            ))
            return ValidationReport(
                is_valid=False,
                total_diagnostics=len(diagnostics),
                errors_count=1,
                warnings_count=0,
                diagnostics=diagnostics,
                summary="Pattern is empty."
            )

        # Rule 1: Sequential unit indices
        expected_idx = ast.units[0].index
        for unit in ast.units:
            if unit.index != expected_idx and expected_idx > 0:
                diagnostics.append(Diagnostic(
                    unit_index=unit.index,
                    line_number=unit.line_number,
                    severity=DiagnosticSeverity.WARNING,
                    rule_code="NON_SEQUENTIAL_INDEX",
                    message=f"Expected {unit.unit_type.value} {expected_idx}, but found {unit.unit_type.value} {unit.index}.",
                    suggested_fix=f"Change header to '{unit.unit_type.capitalize()} {expected_idx}'"
                ))
            expected_idx = unit.index + 1

        # Rule 2: Conservation and Stated Count checks
        prev_unit: PatternUnit = None
        for i, unit in enumerate(ast.units):
            # Check Stated Count vs Computed Produced Count
            if unit.stated_stitch_count is not None:
                if unit.stated_stitch_count != unit.computed_produced_count:
                    diff = unit.computed_produced_count - unit.stated_stitch_count
                    direction = "more" if diff > 0 else "fewer"
                    diagnostics.append(Diagnostic(
                        unit_index=unit.index,
                        line_number=unit.line_number,
                        severity=DiagnosticSeverity.ERROR if abs(diff) > 2 else DiagnosticSeverity.WARNING,
                        rule_code="STATED_COUNT_MISMATCH",
                        message=f"{unit.unit_type.capitalize()} {unit.index} states ({unit.stated_stitch_count} sts) at end, but instructions produce {unit.computed_produced_count} sts ({abs(diff)} {direction}).",
                        suggested_fix=f"Update stated count to ({unit.computed_produced_count}) or adjust stitch repeats.",
                        expected_value=unit.stated_stitch_count,
                        actual_value=unit.computed_produced_count
                    ))

            # Check Consumed vs Previous Produced (for units after unit 1)
            if prev_unit is not None:
                prev_available = prev_unit.computed_produced_count
                consumed = unit.computed_consumed_count
                
                # Check if non-foundation unit consumes more stitches than available
                if prev_available > 0 and consumed > 0 and consumed != prev_available:
                    diff = consumed - prev_available
                    diagnostics.append(Diagnostic(
                        unit_index=unit.index,
                        line_number=unit.line_number,
                        severity=DiagnosticSeverity.WARNING,
                        rule_code="CONSERVATION_MISMATCH",
                        message=f"{unit.unit_type.capitalize()} {unit.index} attempts to work into {consumed} stitches, but previous {prev_unit.unit_type.value} {prev_unit.index} only created {prev_available} stitches.",
                        suggested_fix=f"Verify repeat counts so consumed stitches total {prev_available}.",
                        expected_value=prev_available,
                        actual_value=consumed
                    ))

            prev_unit = unit

        errors_count = sum(1 for d in diagnostics if d.severity == DiagnosticSeverity.ERROR)
        warnings_count = sum(1 for d in diagnostics if d.severity == DiagnosticSeverity.WARNING)
        is_valid = errors_count == 0

        summary = "Pattern is valid with no errors." if is_valid and warnings_count == 0 else (
            f"Found {errors_count} error(s) and {warnings_count} warning(s)."
        )

        return ValidationReport(
            is_valid=is_valid,
            total_diagnostics=len(diagnostics),
            errors_count=errors_count,
            warnings_count=warnings_count,
            diagnostics=diagnostics,
            summary=summary
        )
