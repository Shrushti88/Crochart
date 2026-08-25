"""
Preprocesses raw crochet pattern text into normalized lines.
Handles US/UK translation, abbreviation expansion, comment removal, and clean segmentation.
"""

import re
from typing import List, Tuple, Dict
from ..ontology.schema import TerminologyStandard
from ..ontology.vocabulary import US_TO_UK_MAP, UK_TO_US_MAP

class Preprocessor:
    @staticmethod
    def clean_text(raw_text: str) -> List[Tuple[int, str]]:
        """
        Cleans raw text and returns a list of (1-based line_number, normalized_line).
        Removes comments, blank lines, bullet markers, etc.
        """
        lines = raw_text.splitlines()
        cleaned: List[Tuple[int, str]] = []
        
        for idx, line in enumerate(lines, start=1):
            line_str = line.strip()
            if not line_str:
                continue
            
            # Remove markdown bullets/formatting
            line_str = re.sub(r"^[*\-•#]+\s*", "", line_str)
            # Remove leading/trailing formatting like **
            line_str = line_str.replace("**", "").replace("__", "")
            
            # Normalize whitespace
            line_str = re.sub(r"\s+", " ", line_str).strip()
            
            if line_str:
                cleaned.append((idx, line_str))
                
        return cleaned

    @staticmethod
    def normalize_terms(line: str, source_term: TerminologyStandard = TerminologyStandard.US, target_term: TerminologyStandard = TerminologyStandard.US) -> str:
        """
        Translates crochet terminology if needed (e.g. UK to US or vice versa).
        """
        if source_term == target_term:
            return line
        
        mapping = UK_TO_US_MAP if source_term == TerminologyStandard.UK else US_TO_UK_MAP
        result = line
        
        # Sort keys by length descending to replace multi-word terms first
        for src in sorted(mapping.keys(), key=len, reverse=True):
            tgt = mapping[src]
            pattern = r"\b" + re.escape(src) + r"\b"
            result = re.sub(pattern, tgt, result, flags=re.IGNORECASE)
            
        return result

    @staticmethod
    def standardize_abbreviations(text: str) -> str:
        """
        Standardizes common notation variations like 'sc 2', '2sc', 'sc into next', 'sc in each'.
        """
        norm = text
        # Normalize multiplication repeats like 'x 6', 'x6', '* 6', 'times 6'
        norm = re.sub(r"\b(?:times|time)\b", "x", norm, flags=re.IGNORECASE)
        # Normalize '2 sc' vs 'sc 2' vs '2sc' -> '2 sc'
        norm = re.sub(r"(\d+)\s*(sc|dc|hdc|tr|dtr|ch|sl\s*st|inc|dec)\b", r"\1 \2", norm, flags=re.IGNORECASE)
        # Normalize magic ring variations
        norm = re.sub(r"\b(?:magic\s+circle|magic\s+loop|mr|mc)\b", "magic ring", norm, flags=re.IGNORECASE)
        # Normalize slip stitch variations
        norm = re.sub(r"\bsl\s*st\b|\bslst\b|\bslip\s+stitch\b", "sl st", norm, flags=re.IGNORECASE)
        # Normalize single crochet variations
        norm = re.sub(r"\bsingle\s+crochet\b", "sc", norm, flags=re.IGNORECASE)
        # Normalize double crochet variations
        norm = re.sub(r"\bdouble\s+crochet\b", "dc", norm, flags=re.IGNORECASE)
        # Normalize half double crochet variations
        norm = re.sub(r"\bhalf\s+double\s+crochet\b", "hdc", norm, flags=re.IGNORECASE)
        # Normalize treble crochet variations
        norm = re.sub(r"\btreble\s+crochet\b|\btriple\s+crochet\b", "tr", norm, flags=re.IGNORECASE)
        # Normalize increases
        norm = re.sub(r"\b2\s*sc\s+in\s+(?:the\s+)?(?:next|same)\s+st(?:itch)?\b", "inc", norm, flags=re.IGNORECASE)
        norm = re.sub(r"\b2\s*dc\s+in\s+(?:the\s+)?(?:next|same)\s+st(?:itch)?\b", "dc inc", norm, flags=re.IGNORECASE)
        # Normalize decreases
        norm = re.sub(r"\bsc2tog\b|\bsc\s+2\s+together\b|\bdec\s+sc\b", "dec", norm, flags=re.IGNORECASE)
        norm = re.sub(r"\bdc2tog\b|\bdc\s+2\s+together\b", "dc dec", norm, flags=re.IGNORECASE)
        # Normalize invisible decrease
        norm = re.sub(r"\binv(?:isible)?\s+dec(?:rease)?\b", "inv dec", norm, flags=re.IGNORECASE)
        
        return norm
