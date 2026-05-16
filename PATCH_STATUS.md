# TechnBuddy Patch Status

## TB-01 — Sydney Protocol Core Connection

Status: COMPLETE

TechnBuddy uses the vendored Sydney Protocol Core v0.3 package as its framework layer while remaining a one-input app.

Boundaries preserved:

- one input only;
- no module router;
- no scores or verdicts;
- no certification language;
- no authority claim;
- human judgment remains required.

## TB-02 — Green / Orange / Red Signal Mirror

Status: COMPLETE

TechnBuddy now renders bounded core signals as simple zones:

- GREEN — Helpful signals;
- ORANGE — Check zone;
- RED — High-risk factors;
- Next safe step;
- Your decision.

Implementation notes:

- `Severity.INFO` maps to GREEN.
- `Severity.REVIEW` maps to ORANGE.
- `Severity.WARNING` maps to RED.
- The scan remains rule-based and does not require an LLM.
- No ALETHEIA SANCTUARY / THRESHOLD / ASYLUM states are used.
- Safety-first fail-closed wording remains for immediate danger contexts.

Next likely patch:

- TB-03 — Demo Case Pack / Quick Scan Examples for AI self-certification, suspicious email, institutional letter, DAO proposal, and vulnerable-user AI answer.
