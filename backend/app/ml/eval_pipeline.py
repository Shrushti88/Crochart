"""
ML Evaluation Pipeline for Crochet Pattern Parsing.
Calculates key benchmarks:
1. AST Structure Accuracy
2. Stitch Count Validation Score
3. Unit Parsing Success Rate
4. Graph Topology Consistency
"""

from typing import List, Dict, Any
from ..parser.ast_parser import ASTParser
from ..validator.rules import PatternValidator
from ..layout.graph_builder import ChartGraphBuilder

class PatternEvaluator:
    @classmethod
    def evaluate_dataset(cls, dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not dataset:
            return {
                "total_samples": 0,
                "overall_score": 0.0,
                "ast_accuracy": 0.0,
                "stitch_conservation_rate": 0.0,
                "validation_pass_rate": 0.0,
                "details": []
            }

        total = len(dataset)
        parsed_units_matched = 0
        valid_conservation_count = 0
        validation_passed_count = 0
        graph_structure_matched = 0
        
        details: List[Dict[str, Any]] = []
        parser = ASTParser()

        for item in dataset:
            raw = item.get("written_pattern", "")
            expected_ast = item.get("structured_ast", {})
            expected_chart = item.get("expected_chart", {})

            # Run deterministic parse
            ast = parser.parse(raw)
            validation = PatternValidator.validate(ast)
            chart = ChartGraphBuilder.build(ast)

            # Check unit count match
            expected_units = len(expected_ast.get("units", [])) if expected_ast else None
            units_match = (len(ast.units) == expected_units) if expected_units is not None else True
            if units_match:
                parsed_units_matched += 1

            # Check validation pass
            if validation.is_valid:
                validation_passed_count += 1
            if validation.warnings_count == 0 and validation.errors_count == 0:
                valid_conservation_count += 1

            # Check chart match
            exp_stitches = expected_chart.get("total_stitches") if expected_chart else None
            chart_match = (chart.total_stitches == exp_stitches) if exp_stitches is not None else True
            if chart_match:
                graph_structure_matched += 1

            details.append({
                "title": ast.title,
                "units_count": len(ast.units),
                "total_stitches": chart.total_stitches,
                "is_valid": validation.is_valid,
                "errors_count": validation.errors_count,
                "warnings_count": validation.warnings_count,
                "passed": validation.is_valid and units_match and chart_match
            })

        ast_accuracy = round((parsed_units_matched / total) * 100, 1)
        validation_pass_rate = round((validation_passed_count / total) * 100, 1)
        stitch_conservation_rate = round((valid_conservation_count / total) * 100, 1)
        chart_topology_accuracy = round((graph_structure_matched / total) * 100, 1)
        
        overall_score = round((ast_accuracy + validation_pass_rate + stitch_conservation_rate + chart_topology_accuracy) / 4.0, 1)

        return {
            "total_samples": total,
            "overall_score": overall_score,
            "ast_accuracy": ast_accuracy,
            "validation_pass_rate": validation_pass_rate,
            "stitch_conservation_rate": stitch_conservation_rate,
            "chart_topology_accuracy": chart_topology_accuracy,
            "details": details[:10]  # First 10 samples summary
        }
