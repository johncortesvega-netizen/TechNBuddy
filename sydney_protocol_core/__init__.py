"""Sydney Protocol Core v0.3.

A reusable ethical-governance framework for human-centered apps. It surfaces
review signals, repair questions, response shapes, compact receipts, and
non-throne boundary notes. It never claims final authority.
"""

from .analyzer import CORE_VERSION, MAX_INPUT_CHARS, analyze_text, stable_input_hash
from .boundaries import get_boundary_notes
from .models import AppProfile, BoundaryNote, EvidenceTrace, Language, Reading, ReadingStatus, Receipt, Severity, Signal
from .principles import get_principles, normalize_language
from .profiles import get_profile, list_profiles
from .receipt import create_receipt
from .repair import get_repair_questions
from .validation import validate_reading_boundary, validate_receipt_boundary

__all__ = [
    "CORE_VERSION",
    "MAX_INPUT_CHARS",
    "analyze_text",
    "stable_input_hash",
    "create_receipt",
    "get_boundary_notes",
    "get_principles",
    "normalize_language",
    "get_profile",
    "list_profiles",
    "get_repair_questions",
    "validate_reading_boundary",
    "validate_receipt_boundary",
    "AppProfile",
    "BoundaryNote",
    "EvidenceTrace",
    "Language",
    "Reading",
    "ReadingStatus",
    "Receipt",
    "Severity",
    "Signal",
]
