"""Compact receipt creation for Sydney Protocol Core."""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone

from .analyzer import CORE_VERSION
from .models import Reading, Receipt


def create_receipt(reading: Reading) -> Receipt:
    """Create a deterministic, bounded receipt from a Reading.

    The receipt records the reading shape and input hash. It does not certify
    truth, safety, legality, corruption, legitimacy, or final authority.
    """
    seed = f"{CORE_VERSION}|{reading.profile}|{reading.language.value}|{reading.input_hash}|{reading.status}"
    receipt_id = "spr_" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:20]
    return Receipt(
        receipt_id=receipt_id,
        core_version=CORE_VERSION,
        profile=reading.profile,
        language=reading.language,
        status=reading.status,
        input_hash=reading.input_hash,
        input_preview=reading.input_preview,
        signals=tuple(reading.signals),
        repair_questions=tuple(reading.repair_questions),
        boundary_notes=tuple(reading.boundary_notes),
        metadata={
            "created_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "claim_boundary": "receipt_is_trace_not_certification",
        },
    )
