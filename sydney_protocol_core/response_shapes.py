"""Plain-language response section builder."""

from __future__ import annotations

from .models import BoundaryNote, Language, Signal
from .principles import normalize_language

SECTION_LABELS = {
    Language.EN: {
        "what_i_see": "What I see",
        "possible_pressure": "Possible pressure",
        "what_to_check": "What to check",
        "gentle_option": "Gentle option",
        "boundary_note": "Boundary note",
        "what_the_speech_is_doing": "What the speech is doing",
        "pressure_signals": "Pressure signals",
        "evidence_gaps": "Evidence gaps",
        "questions_before_trusting": "Questions before trusting",
        "claim_being_made": "Claim being made",
        "mechanism_check": "Mechanism check",
        "human_review_issue": "Human review issue",
    },
    Language.NL: {
        "what_i_see": "Wat ik zie",
        "possible_pressure": "Mogelijke druk",
        "what_to_check": "Wat je kunt checken",
        "gentle_option": "Rustige optie",
        "boundary_note": "Grensnotitie",
        "what_the_speech_is_doing": "Wat de speech doet",
        "pressure_signals": "Druksignalen",
        "evidence_gaps": "Bewijsgaten",
        "questions_before_trusting": "Vragen vóór vertrouwen",
        "claim_being_made": "Claim die wordt gemaakt",
        "mechanism_check": "Mechanismecheck",
        "human_review_issue": "Menselijke review",
    },
}


def _signal_summary(signals: list[Signal], language: Language) -> str:
    if not signals:
        return "No obvious pressure signal detected." if language == Language.EN else "Geen duidelijk druksignaal gevonden."
    return "; ".join(signal.label for signal in signals)


def _match_summary(signals: list[Signal], language: Language) -> str:
    matched = [match for signal in signals for match in signal.matches]
    if not matched:
        return "No direct phrase match to show." if language == Language.EN else "Geen directe zinsmatch om te tonen."
    prefix = "Matched phrases: " if language == Language.EN else "Gevonden woorden/zinnen: "
    return prefix + ", ".join(sorted(set(matched)))


def build_sections(
    *,
    shape: tuple[str, ...],
    signals: list[Signal],
    repair_questions: list[str],
    boundary_notes: tuple[BoundaryNote, ...],
    language: str | Language = Language.EN,
) -> dict[str, str]:
    """Build plain response sections for app UIs.

    The sections are intentionally simple. Apps may render them as cards,
    Markdown, chat text, or receipts.
    """
    lang = normalize_language(language)
    labels = SECTION_LABELS[lang]
    signal_summary = _signal_summary(signals, lang)
    match_summary = _match_summary(signals, lang)
    first_boundary = boundary_notes[0].text if boundary_notes else (
        "Human review required." if lang == Language.EN else "Menselijke review blijft nodig."
    )
    questions = " ".join(repair_questions[:4])

    if lang == Language.EN:
        content = {
            "what_i_see": f"I can read this as one bounded situation for review. {match_summary}",
            "possible_pressure": signal_summary,
            "what_to_check": questions or "Ask what context, evidence, or authority is missing.",
            "gentle_option": "Pause, ask for clarity, and choose without pressure. Treat this as a prompt for review, not a verdict.",
            "boundary_note": first_boundary,
            "what_the_speech_is_doing": f"The speech may be shaping belief through these review signals: {signal_summary}",
            "pressure_signals": signal_summary,
            "evidence_gaps": "Check sources, dates, mechanisms, uncertainty, and who benefits.",
            "questions_before_trusting": questions or "What would change your mind? Who benefits? What evidence is missing?",
            "claim_being_made": "Identify the claim before trusting the conclusion.",
            "mechanism_check": "Look for the mechanism behind the promise, safety claim, or authority claim.",
            "human_review_issue": "A person still needs to review context, evidence, and consequences.",
        }
    else:
        content = {
            "what_i_see": f"Ik kan dit lezen als één begrensde situatie voor review. {match_summary}",
            "possible_pressure": signal_summary,
            "what_to_check": questions or "Vraag welke context, welk bewijs of welke bevoegdheid ontbreekt.",
            "gentle_option": "Pauzeer, vraag om helderheid, en kies zonder druk. Behandel dit als reviewprompt, niet als oordeel.",
            "boundary_note": first_boundary,
            "what_the_speech_is_doing": f"De speech kan overtuiging vormen via deze reviewsignalen: {signal_summary}",
            "pressure_signals": signal_summary,
            "evidence_gaps": "Check bronnen, datums, mechanismen, onzekerheid en wie profiteert.",
            "questions_before_trusting": questions or "Wat zou je van mening doen veranderen? Wie profiteert? Welk bewijs ontbreekt?",
            "claim_being_made": "Benoem eerst de claim voordat je de conclusie vertrouwt.",
            "mechanism_check": "Zoek het mechanisme achter de belofte, veiligheidsclaim of autoriteitsclaim.",
            "human_review_issue": "Een mens moet context, bewijs en gevolgen blijven beoordelen.",
        }

    return {labels[key]: content[key] for key in shape if key in labels and key in content}
