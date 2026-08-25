"""
Tokenizer for crochet pattern grammar.
Breaks unit strings into semantic tokens: headers, bracket groups, stitch expressions, and counts.
"""

import re
from typing import List, Optional, Tuple, Dict, Any
from enum import Enum
from ..ontology.schema import UnitType

class TokenType(str, Enum):
    HEADER = "HEADER"
    STITCH_EXPR = "STITCH_EXPR"
    REPEAT_GROUP = "REPEAT_GROUP"
    STATED_COUNT = "STATED_COUNT"
    JOIN = "JOIN"
    TURN = "TURN"

class Token:
    def __init__(self, token_type: TokenType, value: Any, raw: str = "", line_number: int = 1):
        self.token_type = token_type
        self.value = value
        self.raw = raw
        self.line_number = line_number

    def __repr__(self):
        return f"Token({self.token_type}, {self.value}, line={self.line_number})"

class PatternTokenizer:
    # Pattern to match Round/Row header
    HEADER_REGEX = re.compile(
        r"^(?:(round|rnd|r|row)\s*(\d+)|foundation(?:\s+chain|\s+row)?)\s*[:.\-–]?\s*",
        re.IGNORECASE
    )

    # Pattern to match stated stitch count at the end of a line
    STATED_COUNT_REGEX = re.compile(
        r"(?:[\(\[\{]|--|\-\s*)\s*(\d+)\s*(?:sts?|stitches|sc|dc|hdc|tr)?\s*[\)\]\}]?\s*$",
        re.IGNORECASE
    )

    @classmethod
    def extract_header_and_count(cls, line: str, line_number: int) -> Tuple[Optional[UnitType], Optional[int], Optional[int], str]:
        """
        Extracts unit type (ROUND/ROW), index (e.g. 1, 2), stated stitch count (e.g. 12), and remaining instruction body.
        """
        cleaned = line.strip()
        unit_type = None
        unit_index = None
        stated_count = None

        # Check for stated count at end
        count_match = cls.STATED_COUNT_REGEX.search(cleaned)
        if count_match:
            try:
                stated_count = int(count_match.group(1))
                # Strip the count from the line
                cleaned = cleaned[:count_match.start()].strip()
            except ValueError:
                pass

        # Check for Header
        header_match = cls.HEADER_REGEX.match(cleaned)
        if header_match:
            kind_str = (header_match.group(1) or "").lower()
            idx_str = header_match.group(2)
            
            if "row" in kind_str:
                unit_type = UnitType.ROW
            elif "round" in kind_str or "rnd" in kind_str or kind_str == "r":
                unit_type = UnitType.ROUND
            elif "foundation" in cleaned.lower():
                unit_type = UnitType.ROW
                idx_str = "0"
                
            if idx_str is not None:
                unit_index = int(idx_str)
                
            cleaned = cleaned[header_match.end():].strip()

        # If header wasn't found, infer from text
        if unit_type is None:
            if "magic ring" in cleaned.lower() or "in the round" in cleaned.lower() or "join" in cleaned.lower():
                unit_type = UnitType.ROUND
            else:
                unit_type = UnitType.ROUND  # Default to round

        return unit_type, unit_index, stated_count, cleaned

    @classmethod
    def split_top_level_operations(cls, text: str) -> List[str]:
        """
        Splits text by comma, semicolon, or period, respecting nested brackets/parentheses and repeat asterisks.
        """
        chunks: List[str] = []
        current = []
        depth_paren = 0
        depth_bracket = 0
        in_asterisks = False
        
        i = 0
        n = len(text)
        while i < n:
            c = text[i]
            
            if c == '(':
                depth_paren += 1
                current.append(c)
            elif c == ')':
                depth_paren = max(0, depth_paren - 1)
                current.append(c)
            elif c == '[':
                depth_bracket += 1
                current.append(c)
            elif c == ']':
                depth_bracket = max(0, depth_bracket - 1)
                current.append(c)
            elif c == '*':
                in_asterisks = not in_asterisks
                current.append(c)
            elif (c in (',', ';') or (c == '.' and i < n - 1 and not text[i+1].isdigit())) and depth_paren == 0 and depth_bracket == 0 and not in_asterisks:
                piece = "".join(current).strip()
                if piece:
                    chunks.append(piece)
                current = []
            else:
                current.append(c)
            i += 1
            
        final_piece = "".join(current).strip()
        if final_piece:
            chunks.append(final_piece)
            
        return chunks
