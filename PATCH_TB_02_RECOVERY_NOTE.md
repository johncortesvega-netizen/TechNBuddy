# PATCH TB-02 RECOVERY NOTE

## What this patch does

TB-02 updates TechnBuddy into a Green / Orange / Red signal mirror.

The app still uses Sydney Protocol Core v0.3. It now renders the core's bounded signals as simple user-facing zones rather than a chat-style protocol reading.

## Recovery point

If this patch needs to be reverted, restore:

- `app.py`
- `README.md`
- `PATCH_STATUS.md`

from the previous TechnBuddy v0.2 full app zip.

## Safety boundaries

This patch does not add scoring, verdicts, certification, LLM autonomy, legal/medical/political authority, or ALETHEIA taxonomy states.

TechnBuddy remains a review aid only. It shows signals before action; it does not decide.
