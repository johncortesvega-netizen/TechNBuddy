"""Self-checks for apps that claim to use Sydney Protocol Core."""

from __future__ import annotations

from .models import Reading, Receipt

FORBIDDEN_AUTHORITY_PHRASES = (
    "certified true",
    "verified safe",
    "this is corruption",
    "this is illegal",
    "final verdict",
    "officially legitimate",
    "you must obey",
    "gecertificeerd waar",
    "geverifieerd veilig",
    "dit is corruptie",
    "dit is illegaal",
    "definitief oordeel",
    "officieel legitiem",
    "je moet gehoorzamen",
)

REQUIRED_BOUNDARY_KEYS = {"not_authority", "not_decision", "not_certification", "human_review"}


def _boundary_issues(boundary_notes: object, rendered: str) -> list[str]:
    notes = list(boundary_notes)  # type: ignore[arg-type]
    issues: list[str] = []
    present = {note.key for note in notes}
    missing = REQUIRED_BOUNDARY_KEYS - present
    if missing:
        issues.append("Missing required boundary note(s): " + ", ".join(sorted(missing)))
    lowered = rendered.lower()
    for phrase in FORBIDDEN_AUTHORITY_PHRASES:
        if phrase in lowered:
            issues.append(f"Possible authority overclaim phrase in rendered response: {phrase!r}")
    return issues


def validate_reading_boundary(reading: Reading) -> list[str]:
    """Return boundary issues found in a Reading.

    Empty list means no obvious framework-boundary issue was found. This is not
    a certification of safety or truth.
    """
    rendered = "\n".join(reading.response_sections.values())
    return _boundary_issues(reading.boundary_notes, rendered)


def validate_receipt_boundary(receipt: Receipt) -> list[str]:
    """Return boundary issues found in a Receipt."""
    rendered = "\n".join(note.text for note in receipt.boundary_notes)
    rendered += "\n" + receipt.to_dict().get("non_throne_statement", "")
    return _boundary_issues(receipt.boundary_notes, rendered)
