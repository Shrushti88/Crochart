"""
Validation models and diagnostics types for crochet pattern analysis.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

class DiagnosticSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

class Diagnostic(BaseModel):
    unit_index: Optional[int] = None
    line_number: int = 1
    severity: DiagnosticSeverity = DiagnosticSeverity.WARNING
    rule_code: str
    message: str
    suggested_fix: Optional[str] = None
    expected_value: Optional[int] = None
    actual_value: Optional[int] = None

class ValidationReport(BaseModel):
    is_valid: bool = True
    total_diagnostics: int = 0
    errors_count: int = 0
    warnings_count: int = 0
    diagnostics: List[Diagnostic] = Field(default_factory=list)
    summary: str = "Pattern validation passed."
