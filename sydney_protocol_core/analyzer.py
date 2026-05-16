"""Transparent, bounded analyzer for Sydney Protocol Core."""

from __future__ import annotations

import hashlib
import re
from collections.abc import Iterable

from .boundaries import get_boundary_notes
from .lexicons import PHRASES, SIGNAL_DEFINITIONS, SIGNAL_LIMITATIONS
from .models import EvidenceTrace, Language, Reading, Signal
from .principles import get_principles, normalize_language
from .profiles import get_profile
from .repair import get_repair_questions
from .response_shapes import build_sections

MAX_INPUT_CHARS = 120_000
CORE_VERSION = "0.3.0"
_CONTEXT_CHARS = 70
_CONTEXT_GUARDS_EN = (
    "example", "for example", "sample", "quote", "quoted", "warning against", "do not say", "don't say", "avoid saying",
)
_CONTEXT_GUARDS_NL = (
    "voorbeeld", "bijvoorbeeld", "citaat", "geciteerd", "waarschuwing tegen", "zeg niet", "vermijd te zeggen",
)


def _validate_text(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("analyze_text requires text to be a string")
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("analyze_text requires non-empty text")
    if len(cleaned) > MAX_INPUT_CHARS:
        raise ValueError(f"Input too large for Sydney Protocol Core v0.3: {len(cleaned)} chars > {MAX_INPUT_CHARS}")
    return cleaned


def stable_input_hash(text: str) -> str:
    """Return a stable sha256 hash for the normalized input text."""
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()


def _is_context_guarded(context: str, lang: Language) -> bool:
    lowered = context.lower()
    guards = _CONTEXT_GUARDS_NL if lang == Language.NL else _CONTEXT_GUARDS_EN
    return any(guard in lowered for guard in guards)


def _find_matches(text: str, phrases: Iterable[str], *, language: Language) -> list[tuple[str, str]]:
    lowered = text.lower()
    found: list[tuple[str, str]] = []
    for phrase in phrases:
        escaped = re.escape(phrase.lower()).replace(r"\ ", r"\s+")
        pattern = r"(?<!\w)" + escaped + r"(?!\w)"
        match = re.search(pattern, lowered, flags=re.UNICODE)
        if not match:
            continue
        start = max(0, match.start() - _CONTEXT_CHARS)
        end = min(len(text), match.end() + _CONTEXT_CHARS)
        context = text[start:end].strip()
        if _is_context_guarded(context, language):
            continue
        found.append((phrase, context))
    return found


def analyze_text(text: str, *, profile: str = "technbuddy_chat", language: str | Language | None = None) -> Reading:
    """Analyze text for possible Sydney Protocol review signals.

    This function makes no factual finding and no accusation. It returns a
    bounded reading that applications can render for human review.
    """
    cleaned = _validate_text(text)
    lang = normalize_language(language, cleaned)
    app_profile = get_profile(profile)
    phrase_bank = PHRASES[lang]

    signals: list[Signal] = []
    for key in app_profile.preferred_signal_keys:
        match_pairs = _find_matches(cleaned, phrase_bank.get(key, ()), language=lang)
        if not match_pairs:
            continue
        label, description, severity = SIGNAL_DEFINITIONS[key][lang]
        limitation = SIGNAL_LIMITATIONS[lang][key]
        traces = tuple(
            EvidenceTrace(
                phrase=phrase,
                context=context,
                explanation=description,
                limitation=limitation,
            )
            for phrase, context in match_pairs
        )
        signals.append(
            Signal(
                key=key,
                label=label,
                description=description,
                severity=severity,
                matches=tuple(phrase for phrase, _ in match_pairs),
                traces=traces,
            )
        )

    signal_keys = [signal.key for signal in signals]
    repair_questions = get_repair_questions(signal_keys, lang)
    boundary_notes = get_boundary_notes(lang, required_keys=tuple(app_profile.required_boundaries))
    sections = build_sections(
        shape=tuple(app_profile.response_shape),
        signals=signals,
        repair_questions=repair_questions,
        boundary_notes=boundary_notes,
        language=lang,
    )

    return Reading(
        profile=app_profile.key,
        language=lang,
        input_preview=cleaned[:240],
        input_hash=stable_input_hash(cleaned),
        signals=tuple(signals),
        repair_questions=tuple(repair_questions),
        boundary_notes=boundary_notes,
        response_sections=sections,
        principles=get_principles(lang),
        metadata={
            "core_version": CORE_VERSION,
            "profile_display_name": app_profile.display_name,
            "claim_boundary": "signals_only_no_verdict",
            "input_storage_policy": "preview_plus_hash_by_default",
        },
    )
