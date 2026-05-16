"""Repair questions for Sydney Protocol readings."""

from __future__ import annotations

from .models import Language
from .principles import normalize_language

QUESTIONS = {
    Language.EN: {
        "pressure": "Can the person freely pause, refuse, or ask for time?",
        "boundary": "What boundary, consent, or privacy limit should be made explicit?",
        "evidence_gap": "What source, date, mechanism, or counter-evidence is missing?",
        "authority_overclaim": "Who has authority here, and what limits or appeal routes exist?",
        "safety": "Is immediate help, distance, or local emergency support needed?",
        "corruption_pressure": "Who benefits, who oversees it, and what accountability trail exists?",
        "repair_opportunity": "What wording would reduce pressure and restore clarity or dignity?",
    },
    Language.NL: {
        "pressure": "Kan iemand vrij pauzeren, weigeren of om tijd vragen?",
        "boundary": "Welke grens, toestemming of privacyafspraak moet expliciet worden gemaakt?",
        "evidence_gap": "Welke bron, datum, mechanisme of tegeninformatie ontbreekt?",
        "authority_overclaim": "Wie heeft hier bevoegdheid, en welke grenzen of bezwaarroute bestaan er?",
        "safety": "Is directe hulp, afstand of lokale noodhulp nodig?",
        "corruption_pressure": "Wie profiteert, wie houdt toezicht, en welk verantwoordingsspoor bestaat er?",
        "repair_opportunity": "Welke formulering zou druk verminderen en helderheid of waardigheid herstellen?",
    },
}

DEFAULT_QUESTIONS = {
    Language.EN: (
        "What facts are known, and what is still uncertain?",
        "What would reduce pressure and preserve choice?",
        "What human review is still needed?",
    ),
    Language.NL: (
        "Welke feiten zijn bekend, en wat blijft onzeker?",
        "Wat zou druk verminderen en keuze behouden?",
        "Welke menselijke review blijft nodig?",
    ),
}


def get_repair_questions(signal_keys: list[str] | tuple[str, ...], language: str | Language = Language.EN) -> list[str]:
    lang = normalize_language(language)
    questions = QUESTIONS[lang]
    found = [questions[key] for key in signal_keys if key in questions]
    return found if found else list(DEFAULT_QUESTIONS[lang])
