"""
Recursive Descent AST Parser for Crochet Patterns.
Translates tokenized crochet expressions into standard AST representation.
"""

import re
import uuid
from typing import List, Union, Tuple, Optional
from ..ontology.schema import (
    CrochetPatternAST, PatternUnit, StitchInstruction, RepeatGroup,
    StitchType, LoopTarget, UnitType, TerminologyStandard
)
from ..ontology.vocabulary import STITCH_METADATA
from .preprocessor import Preprocessor
from .tokenizer import PatternTokenizer

class ASTParser:
    def __init__(self, terminology: TerminologyStandard = TerminologyStandard.US):
        self.terminology = terminology

    def parse(self, raw_text: str, title: str = "Crochet Pattern") -> CrochetPatternAST:
        """
        Parses full written crochet pattern text into a validated AST.
        """
        cleaned_lines = Preprocessor.clean_text(raw_text)
        units: List[PatternUnit] = []
        is_circular_counts = {"round": 0, "row": 0}
        
        current_inferred_index = 1
        
        for line_num, raw_line in cleaned_lines:
            # Standardize common phrasing & abbreviations
            std_line = Preprocessor.standardize_abbreviations(raw_line)
            
            unit_type, unit_index, stated_count, body = PatternTokenizer.extract_header_and_count(std_line, line_num)
            
            if unit_index is None:
                unit_index = current_inferred_index
            current_inferred_index = unit_index + 1
            
            if unit_type == UnitType.ROUND:
                is_circular_counts["round"] += 1
            else:
                is_circular_counts["row"] += 1
                
            instructions, is_joined, is_turned = self.parse_unit_body(body, line_num)
            
            # Compute total produced & consumed stitches
            produced, consumed = self._calculate_unit_counts(instructions)
            
            unit = PatternUnit(
                unit_type=unit_type or UnitType.ROUND,
                index=unit_index,
                raw_header=raw_line.split(":")[0] if ":" in raw_line else f"{unit_type.capitalize()} {unit_index}",
                raw_text=raw_line,
                instructions=instructions,
                stated_stitch_count=stated_count,
                computed_produced_count=produced,
                computed_consumed_count=consumed,
                is_joined=is_joined,
                is_turned=is_turned,
                line_number=line_num
            )
            units.append(unit)
            
        is_circular = is_circular_counts["round"] >= is_circular_counts["row"]
        
        ast = CrochetPatternAST(
            title=title,
            terminology=self.terminology,
            is_circular=is_circular,
            units=units,
            total_units=len(units),
            raw_text=raw_text,
            metadata={
                "parsed_units_count": len(units),
                "is_circular": is_circular,
            }
        )
        return ast

    def parse_unit_body(self, body: str, line_number: int) -> Tuple[List[Union[StitchInstruction, RepeatGroup]], bool, bool]:
        """
        Parses the body of a round/row into a list of StitchInstruction or RepeatGroup.
        """
        operations = PatternTokenizer.split_top_level_operations(body)
        instructions: List[Union[StitchInstruction, RepeatGroup]] = []
        is_joined = False
        is_turned = False
        
        for op in operations:
            op_str = op.strip()
            if not op_str:
                continue
                
            # Check for join
            if re.search(r"\b(?:join|sl\s*st\s+to\s+first|sl\s*st\s+to\s+join)\b", op_str, re.IGNORECASE):
                is_joined = True
                
            # Check for turn
            if re.search(r"\b(?:turn(?:\s+work)?)\b", op_str, re.IGNORECASE):
                is_turned = True
                
            # Check if this operation is a repeat group: [ ... ] * 6 or * ... * x 6 or ( ... ) * 6
            repeat_match = self._match_repeat_group(op_str)
            if repeat_match:
                inner_text, repeat_count = repeat_match
                sub_instructions, sub_joined, sub_turned = self.parse_unit_body(inner_text, line_number)
                if sub_joined:
                    is_joined = True
                if sub_turned:
                    is_turned = True
                instructions.append(RepeatGroup(
                    id=f"rg_{uuid.uuid4().hex[:8]}",
                    instructions=sub_instructions,
                    repeat_count=repeat_count,
                    raw_text=op_str,
                    line_number=line_number
                ))
                continue
                
            # Otherwise parse single/compound stitch expression
            parsed_stitches = self._parse_stitch_expression(op_str, line_number)
            instructions.extend(parsed_stitches)
            
        return instructions, is_joined, is_turned

    def _match_repeat_group(self, text: str) -> Optional[Tuple[str, int]]:
        """
        Matches repeat notations such as:
        - [sc, inc] * 6
        - [2 sc, inc] x 6
        - *sc 1, inc* 6 times
        - *(sc, inc)* x 6
        - (sc, inc) * 6
        """
        # Bracket repeat: [ ... ] * N
        bracket_pattern = r"^\[(.*?)\]\s*(?:[\*xX]|times|time)?\s*(\d+)?\s*(?:times|time)?$"
        m = re.match(bracket_pattern, text.strip())
        if m:
            inner = m.group(1).strip()
            count = int(m.group(2)) if m.group(2) else 1
            return inner, count

        # Asterisk repeat: * ... * N times / * ... * x N
        asterisk_pattern = r"^\*(.*?)\*\s*(?:[\*xX]|times|time)?\s*(\d+)?\s*(?:times|time)?$"
        m = re.match(asterisk_pattern, text.strip())
        if m:
            inner = m.group(1).strip()
            count = int(m.group(2)) if m.group(2) else 1
            return inner, count

        # Parentheses repeat: ( ... ) * N (only if it has a multiplier at end > 1)
        paren_pattern = r"^\((.*?)\)\s*(?:[\*xX]|times|time)\s*(\d+)\s*(?:times|time)?$"
        m = re.match(paren_pattern, text.strip())
        if m:
            inner = m.group(1).strip()
            count = int(m.group(2))
            return inner, count

        return None

    def _parse_stitch_expression(self, text: str, line_number: int) -> List[StitchInstruction]:
        """
        Parses a single stitch expression like:
        - 'magic ring, 6 sc' or 'mr 6'
        - '6 sc' or 'sc 6' or 'sc in next 6 sts'
        - 'inc in each st around' / 'inc in next 6 sts' / '6 inc'
        - '2 sc in same st'
        - 'ch 3 (counts as dc)' / 'ch 1'
        - 'sc in BLO' / 'dc in FLO'
        - 'dc2tog' / 'dec 3'
        - 'puff' / 'popcorn' / 'picot'
        """
        results: List[StitchInstruction] = []
        clean = text.strip()

        # Check loop modifier (BLO / FLO)
        target_loop = LoopTarget.BOTH
        if re.search(r"\b(blo|back\s+loop(?:\s+only)?)\b", clean, re.IGNORECASE):
            target_loop = LoopTarget.BLO
        elif re.search(r"\b(flo|front\s+loop(?:\s+only)?)\b", clean, re.IGNORECASE):
            target_loop = LoopTarget.FLO

        # Check for Magic Ring starter: "magic ring, 6 sc" or "mr 6" or "6 sc in magic ring"
        mr_in_match = re.search(r"(\d+)\s*(sc|dc|hdc)\s+(?:in|into)\s+(?:the\s+)?magic\s+ring", clean, re.IGNORECASE)
        if mr_in_match:
            count = int(mr_in_match.group(1))
            st_type = StitchType(mr_in_match.group(2).lower())
            results.append(StitchInstruction(
                id=f"st_{uuid.uuid4().hex[:8]}",
                stitch_type=StitchType.MAGIC_RING,
                count=1,
                target_stitch_count=0,
                produced_stitch_count=0,
                raw_text="magic ring",
                line_number=line_number
            ))
            results.append(StitchInstruction(
                id=f"st_{uuid.uuid4().hex[:8]}",
                stitch_type=st_type,
                count=count,
                target_stitch_count=0,
                produced_stitch_count=count,
                raw_text=clean,
                line_number=line_number
            ))
            return results

        mr_with_count = re.search(r"(?:magic\s+ring|mr|mc)\s*(?:with\s*)(\d+)\s*(sc|dc|hdc)?", clean, re.IGNORECASE)
        mr_short = re.match(r"^(?:mr|mc)\s*(\d+)$", clean, re.IGNORECASE)
        if mr_with_count or mr_short:
            count = int(mr_with_count.group(1)) if mr_with_count else int(mr_short.group(1))
            st_str = mr_with_count.group(2) if mr_with_count and mr_with_count.group(2) else "sc"
            st_type = StitchType(st_str.lower())
            results.append(StitchInstruction(
                id=f"st_{uuid.uuid4().hex[:8]}",
                stitch_type=StitchType.MAGIC_RING,
                count=1,
                target_stitch_count=0,
                produced_stitch_count=0,
                raw_text="magic ring",
                line_number=line_number
            ))
            results.append(StitchInstruction(
                id=f"st_{uuid.uuid4().hex[:8]}",
                stitch_type=st_type,
                count=count,
                target_stitch_count=0,
                produced_stitch_count=count,
                raw_text=clean,
                line_number=line_number
            ))
            return results

        if clean.lower() in ("magic ring", "mr", "mc", "magic circle", "magic loop"):
            results.append(StitchInstruction(
                id=f"st_{uuid.uuid4().hex[:8]}",
                stitch_type=StitchType.MAGIC_RING,
                count=1,
                target_stitch_count=0,
                produced_stitch_count=0,
                raw_text="magic ring",
                line_number=line_number
            ))
            return results

        # Check for multiple stitches in same stitch: "(sc, 2 dc, sc) in same st" or "3 dc in next st"
        same_st_match = re.search(r"(\d+)\s*(sc|dc|hdc|tr)\s+(?:in|into)\s+(?:the\s+)?(?:same|next)\s+st", clean, re.IGNORECASE)
        if same_st_match:
            count = int(same_st_match.group(1))
            st_name = same_st_match.group(2).lower()
            st_enum = StitchType.DC_INC if (st_name == "dc" and count == 2) else (StitchType.INC if (st_name == "sc" and count == 2) else StitchType(st_name))
            results.append(StitchInstruction(
                id=f"st_{uuid.uuid4().hex[:8]}",
                stitch_type=st_enum,
                count=1,
                target_loop=target_loop,
                in_same_stitch=True,
                target_stitch_count=1,
                produced_stitch_count=count,
                raw_text=clean,
                line_number=line_number
            ))
            return results

        # Check for Foundation / Starting Chain: "ch 12", "chain 24"
        ch_match = re.search(r"\b(?:ch|chain)\s*(\d+)\b", clean, re.IGNORECASE)
        if ch_match:
            ch_count = int(ch_match.group(1))
            results.append(StitchInstruction(
                id=f"st_{uuid.uuid4().hex[:8]}",
                stitch_type=StitchType.CH,
                count=ch_count,
                target_loop=target_loop,
                target_stitch_count=0,
                produced_stitch_count=ch_count,
                raw_text=clean,
                line_number=line_number
            ))
            return results

        # Check for Increases: "inc", "2 inc", "inc in next 3 sts", "dc inc", "hdc inc"
        inc_match = re.search(r"(?:(\d+)\s*)?(dc\s+inc|hdc\s+inc|inc)(?:\s+(?:in\s+next\s+(\d+)\s+sts?|(\d+)\s+times))?", clean, re.IGNORECASE)
        if inc_match and any(x in clean.lower() for x in ["inc", "dc inc", "hdc inc"]):
            inc_kind = inc_match.group(2).lower().replace(" ", "_")
            st_type = StitchType(inc_kind)
            c1 = int(inc_match.group(1)) if inc_match.group(1) else 1
            c2 = int(inc_match.group(3)) if inc_match.group(3) else (int(inc_match.group(4)) if inc_match.group(4) else 1)
            total_count = max(c1, c2)
            meta = STITCH_METADATA.get(st_type, {})
            results.append(StitchInstruction(
                id=f"st_{uuid.uuid4().hex[:8]}",
                stitch_type=st_type,
                count=total_count,
                target_loop=target_loop,
                target_stitch_count=meta.get("consumed", 1) * total_count,
                produced_stitch_count=meta.get("produced", 2) * total_count,
                raw_text=clean,
                line_number=line_number
            ))
            return results

        # Check for Decreases: "dec", "sc2tog", "dc2tog", "dc dec", "dec in next 3 sts", "inv dec"
        dec_match = re.search(r"(?:(\d+)\s*)?(inv\s+dec|dc\s+dec|dc2tog|hdc\s+dec|hdc2tog|sc2tog|dec)(?:\s+(?:in\s+next\s+(\d+)\s+sts?|(\d+)\s+times))?", clean, re.IGNORECASE)
        if dec_match and any(x in clean.lower() for x in ["dec", "sc2tog", "dc2tog", "inv dec", "dc dec"]):
            dec_kind = dec_match.group(2).lower()
            if "dc" in dec_kind:
                st_type = StitchType.DC_DEC
            elif "hdc" in dec_kind:
                st_type = StitchType.HDC_DEC
            elif "inv" in dec_kind:
                st_type = StitchType.INV_DEC
            else:
                st_type = StitchType.DEC
                
            c1 = int(dec_match.group(1)) if dec_match.group(1) else 1
            c2 = int(dec_match.group(3)) if dec_match.group(3) else (int(dec_match.group(4)) if dec_match.group(4) else 1)
            total_count = max(c1, c2)
            meta = STITCH_METADATA.get(st_type, {})
            results.append(StitchInstruction(
                id=f"st_{uuid.uuid4().hex[:8]}",
                stitch_type=st_type,
                count=total_count,
                target_loop=target_loop,
                target_stitch_count=meta.get("consumed", 2) * total_count,
                produced_stitch_count=meta.get("produced", 1) * total_count,
                raw_text=clean,
                line_number=line_number
            ))
            return results

        # Check for Slip Stitch
        slst_match = re.search(r"(?:(\d+)\s*)?sl\s*st(?:\s+in\s+next\s+(\d+)\s+sts?)?", clean, re.IGNORECASE)
        if slst_match and "sl st" in clean.lower():
            c1 = int(slst_match.group(1)) if slst_match.group(1) else 1
            c2 = int(slst_match.group(2)) if slst_match.group(2) else 1
            count = max(c1, c2)
            results.append(StitchInstruction(
                id=f"st_{uuid.uuid4().hex[:8]}",
                stitch_type=StitchType.SL_ST,
                count=count,
                target_loop=target_loop,
                target_stitch_count=count,
                produced_stitch_count=0,
                raw_text=clean,
                line_number=line_number
            ))
            return results

        # Check for standard basic stitches: sc, hdc, dc, tr, dtr, puff, popcorn, picot, skip
        basic_pattern = r"(?:(\d+)\s*)?(sc|hdc|dc|tr|dtr|puff|popcorn|bobble|cluster|picot|sk|skip)(?:\s+(?:in\s+next\s+(\d+)\s+sts?|(\d+)))?"
        m = re.search(basic_pattern, clean, re.IGNORECASE)
        if m:
            st_raw = m.group(2).lower()
            if st_raw in ("sk", "skip"):
                st_type = StitchType.SKIP
            else:
                st_type = StitchType(st_raw)
                
            c1 = int(m.group(1)) if m.group(1) else 1
            c2 = int(m.group(3)) if m.group(3) else (int(m.group(4)) if m.group(4) else 1)
            count = max(c1, c2)
            
            meta = STITCH_METADATA.get(st_type, {})
            results.append(StitchInstruction(
                id=f"st_{uuid.uuid4().hex[:8]}",
                stitch_type=st_type,
                count=count,
                target_loop=target_loop,
                target_stitch_count=meta.get("consumed", 1) * count,
                produced_stitch_count=meta.get("produced", 1) * count,
                raw_text=clean,
                line_number=line_number
            ))
            return results

        # Fallback single sc if unrecognized token to prevent crashes
        results.append(StitchInstruction(
            id=f"st_{uuid.uuid4().hex[:8]}",
            stitch_type=StitchType.SC,
            count=1,
            target_loop=target_loop,
            target_stitch_count=1,
            produced_stitch_count=1,
            raw_text=clean,
            line_number=line_number
        ))
        return results

    def _calculate_unit_counts(self, instructions: List[Union[StitchInstruction, RepeatGroup]]) -> Tuple[int, int]:
        """
        Recursively calculates (produced_count, consumed_count) for a list of instructions.
        """
        total_produced = 0
        total_consumed = 0
        
        for inst in instructions:
            if isinstance(inst, RepeatGroup):
                sub_p, sub_c = self._calculate_unit_counts(inst.instructions)
                total_produced += sub_p * inst.repeat_count
                total_consumed += sub_c * inst.repeat_count
            elif isinstance(inst, StitchInstruction):
                total_produced += inst.produced_stitch_count
                total_consumed += inst.target_stitch_count
                
        return total_produced, total_consumed
