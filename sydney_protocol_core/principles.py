"""Shared Sydney Protocol principles in plain public language."""

from __future__ import annotations

from .models import Language

PRINCIPLES: dict[Language, tuple[str, ...]] = {
    Language.EN: (
        "Facts before guesses.",
        "Care before control.",
        "Boundaries before pressure.",
        "Safety before pride.",
        "Options, not orders.",
        "Human judgment remains required.",
    ),
    Language.NL: (
        "Feiten vóór aannames.",
        "Zorg vóór controle.",
        "Grenzen vóór druk.",
        "Veiligheid vóór trots.",
        "Opties, geen bevelen.",
        "Menselijk oordeel blijft nodig.",
    ),
}


def normalize_language(language: str | Language | None = None, text: str = "") -> Language:
    """Normalize language to EN/NL.

    Explicit language wins. Without it, a small deterministic heuristic is used.
    """
    if isinstance(language, Language):
        return language
    if language:
        value = language.lower().strip()
        if value.startswith("nl") or value in {"dutch", "nederlands"}:
            return Language.NL
        if value.startswith("en") or value in {"english"}:
            return Language.EN

    lowered = f" {text.lower()} "
    nl_markers = (" je ", " jij ", " niet ", " geen ", " moet ", " iedereen ", " vertrouwen ", " bezwaar ")
    return Language.NL if any(marker in lowered for marker in nl_markers) else Language.EN


def get_principles(language: str | Language = Language.EN) -> tuple[str, ...]:
    """Return public principles for the selected language."""
    return PRINCIPLES[normalize_language(language)]
