"""Typed data models for Sydney Protocol Core.

The core is intentionally bounded: it produces review signals, repair prompts,
receipts, and response sections for human interpretation. It does not establish
truth, guilt, intent, illegality, corruption, safety, legitimacy, or final
authority.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Mapping, Sequence


class Language(str, Enum):
    """Supported public-language packs."""

    EN = "en"
    NL = "nl"


class Severity(str, Enum):
    """Signal severity is a review priority, not a verdict."""

    INFO = "info"
    REVIEW = "review"
    WARNING = "warning"


class ReadingStatus(str, Enum):
    """Bounded status values returned by the core."""

    NO_OBVIOUS_SIGNAL = "No obvious pressure signal detected"
    REVIEW_SUGGESTED = "Review suggested"
    BOUNDARY_WARNING = "Boundary warning"
    INCONCLUSIVE = "Inconclusive"


@dataclass(frozen=True)
class EvidenceTrace:
    """Transparent trace for a signal match.

    This is not proof of intent or wrongdoing. It tells an app which phrase was
    matched, how it is bounded, and which short context can be shown for human
    review.
    """

    phrase: str
    context: str
    explanation: str
    limitation: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class Signal:
    """A possible review signal surfaced from input text.

    `matches` and `traces` contain transparent phrase matches only. They are not
    evidence of intent, guilt, corruption, illegality, or truth.
    """

    key: str
    label: str
    description: str
    severity: Severity = Severity.REVIEW
    matches: Sequence[str] = field(default_factory=tuple)
    traces: Sequence[EvidenceTrace] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["severity"] = self.severity.value
        data["matches"] = list(self.matches)
        data["traces"] = [trace.to_dict() for trace in self.traces]
        return data


@dataclass(frozen=True)
class BoundaryNote:
    """Mandatory non-throne language for Sydney Protocol applications."""

    key: str
    text: str

    def to_dict(self) -> dict[str, str]:
        return {"key": self.key, "text": self.text}


@dataclass(frozen=True)
class AppProfile:
    """Defines how an application uses the Sydney Protocol Core."""

    key: str
    display_name: str
    purpose: str
    response_shape: Sequence[str]
    preferred_signal_keys: Sequence[str]
    required_boundaries: Sequence[str] = field(
        default_factory=lambda: ("not_authority", "not_decision", "not_certification", "human_review")
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "display_name": self.display_name,
            "purpose": self.purpose,
            "response_shape": list(self.response_shape),
            "preferred_signal_keys": list(self.preferred_signal_keys),
            "required_boundaries": list(self.required_boundaries),
        }


@dataclass(frozen=True)
class Reading:
    """A bounded reading produced by the framework."""

    profile: str
    language: Language
    input_preview: str
    input_hash: str
    signals: Sequence[Signal]
    repair_questions: Sequence[str]
    boundary_notes: Sequence[BoundaryNote]
    response_sections: Mapping[str, str]
    principles: Sequence[str] = field(default_factory=tuple)
    metadata: Mapping[str, str] = field(default_factory=dict)

    @property
    def status(self) -> str:
        if not self.input_preview.strip():
            return ReadingStatus.INCONCLUSIVE.value
        if any(signal.severity == Severity.WARNING for signal in self.signals):
            return ReadingStatus.BOUNDARY_WARNING.value
        if self.signals:
            return ReadingStatus.REVIEW_SUGGESTED.value
        return ReadingStatus.NO_OBVIOUS_SIGNAL.value

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "profile": self.profile,
            "language": self.language.value,
            "input_preview": self.input_preview,
            "input_hash": self.input_hash,
            "signals": [signal.to_dict() for signal in self.signals],
            "repair_questions": list(self.repair_questions),
            "boundary_notes": [note.to_dict() for note in self.boundary_notes],
            "response_sections": dict(self.response_sections),
            "principles": list(self.principles),
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class Receipt:
    """Compact review receipt for traceable app integration.

    The receipt stores a hash and preview by default. It does not certify the
    input or the reading.
    """

    receipt_id: str
    core_version: str
    profile: str
    language: Language
    status: str
    input_hash: str
    input_preview: str
    signals: Sequence[Signal]
    repair_questions: Sequence[str]
    boundary_notes: Sequence[BoundaryNote]
    metadata: Mapping[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "receipt_id": self.receipt_id,
            "core_version": self.core_version,
            "profile": self.profile,
            "language": self.language.value,
            "status": self.status,
            "input_hash": self.input_hash,
            "input_preview": self.input_preview,
            "signals": [signal.to_dict() for signal in self.signals],
            "repair_questions": list(self.repair_questions),
            "boundary_notes": [note.to_dict() for note in self.boundary_notes],
            "metadata": dict(self.metadata),
            "non_throne_statement": "This receipt records bounded review signals only; it is not certification, authority, or proof.",
        }
