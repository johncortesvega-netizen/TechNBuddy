"""Mandatory non-throne boundaries for Sydney Protocol apps."""

from __future__ import annotations

from .models import BoundaryNote, Language
from .principles import normalize_language

BOUNDARIES: dict[Language, tuple[BoundaryNote, ...]] = {
    Language.EN: (
        BoundaryNote("not_authority", "This is a review aid, not an authority."),
        BoundaryNote("not_decision", "It gives options and questions, not final decisions."),
        BoundaryNote("not_certification", "It does not certify truth, safety, legality, corruption, or legitimacy."),
        BoundaryNote("human_review", "Human judgment and context remain required."),
        BoundaryNote("not_emergency", "It is not emergency, medical, legal, political, or institutional advice."),
    ),
    Language.NL: (
        BoundaryNote("not_authority", "Dit is een hulpmiddel voor review, geen autoriteit."),
        BoundaryNote("not_decision", "Het geeft opties en vragen, geen definitieve beslissingen."),
        BoundaryNote("not_certification", "Het certificeert geen waarheid, veiligheid, legaliteit, corruptie of legitimiteit."),
        BoundaryNote("human_review", "Menselijk oordeel en context blijven nodig."),
        BoundaryNote("not_emergency", "Het is geen noodhulp, medisch, juridisch, politiek of institutioneel advies."),
    ),
}


def get_boundary_notes(language: str | Language = Language.EN, *, required_keys: tuple[str, ...] | None = None) -> tuple[BoundaryNote, ...]:
    """Return mandatory boundary notes for an app response."""
    notes = BOUNDARIES[normalize_language(language)]
    if required_keys is None:
        return notes
    required = set(required_keys)
    return tuple(note for note in notes if note.key in required)
