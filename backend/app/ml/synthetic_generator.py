"""
Synthetic Crochet Pattern Generator for ML training and benchmarking.
Procedurally generates diverse, grammatically sound crochet patterns with varying phrasing and complexity.
"""

import random
from typing import List, Dict, Any
from ..parser.preprocessor import Preprocessor
from ..parser.ast_parser import ASTParser
from ..layout.graph_builder import ChartGraphBuilder

class SyntheticPatternGenerator:
    STITCH_TYPES = ["sc", "hdc", "dc", "tr"]
    REPEAT_SYNTAXES = ["brackets", "asterisks", "parentheses"]
    COUNT_FORMATS = ["parens", "brackets", "dashes", "none"]

    @classmethod
    def generate_amigurumi_sphere(cls, start_count: int = 6, max_rounds: int = 8, phrasing_style: str = "random") -> Dict[str, Any]:
        """
        Generates a valid spherical amigurumi pattern with increases, even rounds, and decreases.
        """
        repeat_syntax = random.choice(cls.REPEAT_SYNTAXES) if phrasing_style == "random" else phrasing_style
        count_format = random.choice(cls.COUNT_FORMATS)
        
        lines = []
        # Round 1
        lines.append(f"Round 1: Magic ring, {start_count} sc {cls._format_count(start_count, count_format)}")
        
        # Round 2
        inc_phrase = cls._format_repeat("inc", start_count, repeat_syntax)
        curr_count = start_count * 2
        lines.append(f"Round 2: {inc_phrase} {cls._format_count(curr_count, count_format)}")
        
        # Expansion rounds
        expand_steps = (max_rounds - 4) // 2
        for r in range(1, expand_steps + 1):
            curr_rnd = r + 2
            st_part = f"{r} sc" if r > 1 else "sc"
            phrase = cls._format_repeat(f"{st_part}, inc", start_count, repeat_syntax)
            curr_count += start_count
            lines.append(f"Round {curr_rnd}: {phrase} {cls._format_count(curr_count, count_format)}")

        # Even rounds
        even_rnd_1 = len(lines) + 1
        lines.append(f"Round {even_rnd_1}: {curr_count} sc {cls._format_count(curr_count, count_format)}")
        
        # Decrease rounds
        for r in range(expand_steps, 0, -1):
            curr_rnd = len(lines) + 1
            st_part = f"{r} sc" if r > 1 else "sc"
            phrase = cls._format_repeat(f"{st_part}, dec", start_count, repeat_syntax)
            curr_count -= start_count
            lines.append(f"Round {curr_rnd}: {phrase} {cls._format_count(curr_count, count_format)}")

        # Final close round
        final_rnd = len(lines) + 1
        dec_phrase = cls._format_repeat("dec", start_count, repeat_syntax)
        curr_count -= start_count
        lines.append(f"Round {final_rnd}: {dec_phrase} {cls._format_count(curr_count, count_format)}")

        raw_pattern = "\n".join(lines)
        return cls._build_sample_payload(raw_pattern, "Synthetic Amigurumi Sphere", is_circular=True)

    @classmethod
    def generate_flat_circle(cls, stitch: str = "dc", start_count: int = 12, total_rounds: int = 4) -> Dict[str, Any]:
        """
        Generates a flat expanding circular motif in dc or hdc.
        """
        repeat_syntax = random.choice(cls.REPEAT_SYNTAXES)
        count_format = random.choice(cls.COUNT_FORMATS)
        inc_name = f"{stitch} inc" if stitch != "sc" else "inc"
        
        lines = [f"Round 1: Magic ring, {start_count} {stitch}, sl st to join {cls._format_count(start_count, count_format)}"]
        curr_count = start_count

        for r in range(1, total_rounds):
            curr_rnd = r + 1
            if r == 1:
                phrase = cls._format_repeat(inc_name, start_count, repeat_syntax)
            else:
                st_part = f"{r-1} {stitch}" if (r-1) > 1 else stitch
                phrase = cls._format_repeat(f"{st_part}, {inc_name}", start_count, repeat_syntax)
            curr_count += start_count
            lines.append(f"Round {curr_rnd}: {phrase}, sl st to join {cls._format_count(curr_count, count_format)}")

        raw_pattern = "\n".join(lines)
        return cls._build_sample_payload(raw_pattern, f"Synthetic Flat {stitch.upper()} Circle", is_circular=True)

    @classmethod
    def generate_row_fabric(cls, width: int = 20, total_rows: int = 4, stitch: str = "sc") -> Dict[str, Any]:
        """
        Generates a linear row swatch.
        """
        count_format = random.choice(cls.COUNT_FORMATS)
        lines = [f"Row 1: Ch {width}, turn {cls._format_count(width, count_format)}"]
        st_count = width - 1
        
        for r in range(2, total_rows + 2):
            modifier = " in BLO" if random.random() > 0.5 else ""
            lines.append(f"Row {r}: Ch 1, {st_count} {stitch}{modifier}, turn {cls._format_count(st_count, count_format)}")

        raw_pattern = "\n".join(lines)
        return cls._build_sample_payload(raw_pattern, f"Synthetic {stitch.upper()} Row Swatch", is_circular=False)

    @classmethod
    def generate_batch(cls, count: int = 20) -> List[Dict[str, Any]]:
        """
        Generates a diverse batch of synthetic crochet patterns.
        """
        dataset: List[Dict[str, Any]] = []
        for i in range(count):
            choice = random.choice(["amigurumi", "flat_circle", "row_fabric"])
            if choice == "amigurumi":
                st_count = random.choice([6, 8])
                rnds = random.choice([6, 8, 10])
                sample = cls.generate_amigurumi_sphere(start_count=st_count, max_rounds=rnds)
            elif choice == "flat_circle":
                st = random.choice(["dc", "hdc", "sc"])
                start = 12 if st == "dc" else (10 if st == "hdc" else 6)
                sample = cls.generate_flat_circle(stitch=st, start_count=start, total_rounds=random.randint(3, 5))
            else:
                width = random.choice([15, 20, 25])
                sample = cls.generate_row_fabric(width=width, total_rows=random.randint(3, 6), stitch=random.choice(["sc", "hdc", "dc"]))
            dataset.append(sample)
        return dataset

    @classmethod
    def _format_repeat(cls, inner: str, count: int, syntax: str) -> str:
        if syntax == "brackets":
            return f"[{inner}] * {count}"
        elif syntax == "asterisks":
            return f"*{inner}* {count} times"
        else:
            return f"({inner}) * {count}"

    @classmethod
    def _format_count(cls, count: int, format_type: str) -> str:
        if format_type == "parens":
            return f"({count})"
        elif format_type == "brackets":
            return f"[{count} sts]"
        elif format_type == "dashes":
            return f"-- {count} sts"
        return ""

    @classmethod
    def _build_sample_payload(cls, raw_pattern: str, title: str, is_circular: bool) -> Dict[str, Any]:
        parser = ASTParser()
        ast = parser.parse(raw_pattern, title=title)
        chart = ChartGraphBuilder.build(ast)
        
        return {
            "written_pattern": raw_pattern,
            "normalized_pattern": "\n".join([Preprocessor.standardize_abbreviations(line) for _, line in Preprocessor.clean_text(raw_pattern)]),
            "structured_ast": ast.model_dump(),
            "expected_chart": {
                "total_stitches": chart.total_stitches,
                "units_count": chart.units_count,
                "is_circular": chart.is_circular,
                "nodes_count": len(chart.nodes),
                "links_count": len(chart.links)
            }
        }
