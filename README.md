# TechnBuddy v0.5.1

TechnBuddy is a **quick Green / Orange / Red signal mirror built on Sydney Protocol Core v0.3**.

It helps a user paste one message, AI answer, email, form text, or situation and quickly see bounded review signals before acting. The core scan is rule-based: it groups helpful signals, check-zone signals, and high-risk factors without requiring an LLM.

TechnBuddy does **not** decide for the user. It shows signals, repair questions, and one safer next step for human review.

## Core posture

- One input only.
- No module router.
- No scores.
- No verdicts.
- No certification.
- No final authority.
- Human judgment remains required.

Visible principles:

- Facts before guesses.
- Care before control.
- Boundaries before pressure.
- Safety before pride.
- Green signals, orange checks, red flags, your decision.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Patch TB-02

This patch pivots TechnBuddy from a chat-style protocol reading to a Green / Orange / Red signal mirror.

Changes:

- Maps Sydney Protocol Core severities into TechnBuddy zones: `info` → GREEN, `review` → ORANGE, `warning` → RED.
- Replaces the old "What I see / Possible pressure" reply shape with GREEN, ORANGE, RED, Next safe step, and Your decision.
- Updates the app identity to "Green signals. Orange checks. Red flags. Your decision."
- Keeps the scan bounded, rule-based, and non-authoritative.
- Keeps emergency/safety fail-closed wording as a small local overlay.

## Boundary

TechnBuddy is not therapy, emergency response, legal advice, medical advice, political authority, certification, or proof. It is a quick signal mirror for bounded review and human interpretation. It does not output ALETHEIA states such as SANCTUARY, THRESHOLD, or ASYLUM.
