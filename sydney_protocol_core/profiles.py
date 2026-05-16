"""Application profiles built from the Sydney Protocol Core."""

from __future__ import annotations

from .models import AppProfile

TECHNBUDDY_PROFILE = AppProfile(
    key="technbuddy_chat",
    display_name="TechnBuddy Chat",
    purpose="A single friendly chatbox that applies the Sydney Protocol to one situation at a time.",
    response_shape=("what_i_see", "possible_pressure", "what_to_check", "gentle_option", "boundary_note"),
    preferred_signal_keys=("pressure", "boundary", "evidence_gap", "authority_overclaim", "safety", "corruption_pressure", "repair_opportunity"),
)

SPEECH_READER_PROFILE = AppProfile(
    key="speech_reader",
    display_name="Speech Reader",
    purpose="A rhetoric-pressure reader for speeches. It is not a fact-checker and not voting advice.",
    response_shape=("what_the_speech_is_doing", "pressure_signals", "evidence_gaps", "questions_before_trusting", "boundary_note"),
    preferred_signal_keys=("pressure", "evidence_gap", "authority_overclaim", "corruption_pressure", "boundary", "repair_opportunity"),
)

AI_CLAIM_PROFILE = AppProfile(
    key="ai_claim_reader",
    display_name="AI Claim Reader",
    purpose="A reader for AI/product claims, mechanism gaps, overclaim risk, and human-review needs.",
    response_shape=("claim_being_made", "mechanism_check", "evidence_gaps", "human_review_issue", "boundary_note"),
    preferred_signal_keys=("evidence_gap", "authority_overclaim", "safety", "boundary", "corruption_pressure", "repair_opportunity"),
)

RECEIPT_READER_PROFILE = AppProfile(
    key="receipt_reader",
    display_name="Receipt Reader",
    purpose="A reader for structured outputs and audit receipts. It checks coherence and boundaries, not truth.",
    response_shape=("what_i_see", "possible_pressure", "what_to_check", "gentle_option", "boundary_note"),
    preferred_signal_keys=("evidence_gap", "authority_overclaim", "corruption_pressure", "repair_opportunity"),
)

PROFILES = {
    profile.key: profile
    for profile in (TECHNBUDDY_PROFILE, SPEECH_READER_PROFILE, AI_CLAIM_PROFILE, RECEIPT_READER_PROFILE)
}


def get_profile(key: str = "technbuddy_chat") -> AppProfile:
    """Return a known app profile."""
    try:
        return PROFILES[key]
    except KeyError as exc:
        known = ", ".join(sorted(PROFILES))
        raise ValueError(f"Unknown Sydney Protocol profile: {key!r}. Known profiles: {known}") from exc


def list_profiles() -> tuple[AppProfile, ...]:
    """Return all bundled profiles."""
    return tuple(PROFILES.values())
