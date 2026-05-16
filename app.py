from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List

import streamlit as st

from sydney_protocol_core import analyze_text, create_receipt
from sydney_protocol_core.models import Severity


APP_VERSION = "TechnBuddy v0.5.1"
ASSET_DIR = Path(__file__).parent / "assets"
MASCOT_PATH = ASSET_DIR / "technbuddy_mascot.png"


# TechnBuddy keeps a small local safety overlay for obvious high-urgency moments.
# The Sydney Protocol Core provides the reusable framework reading; this overlay
# only controls fail-closed wording for danger contexts in the chat UI.
DEATH_IDIOM_PATTERNS = [
    r"\bi could die\b.*\b(embarrass|embarrassed|awkward|cringe)\b",
    r"\bdying (laughing|of laughter)\b",
    r"\bi'?m dead\b",
    r"\bdead tired\b",
    r"\bi died\b.*\b(laugh|laughing|cringe|embarrass)\b",
]

SELF_HARM_INTENT_PATTERNS = [
    r"\bi want to die\b",
    r"\bi want to kill myself\b",
    r"\bi'?m going to kill myself\b",
    r"\bi might kill myself\b",
    r"\bi'?m going to jump\b",
    r"\bi want to jump off\b",
    r"\bi can'?t do this anymore\b",
    r"\bi don'?t want to be here\b",
    r"\bend it all\b",
]

RISK_ACTIVITY_TERMS = [
    "bungee", "bungee jumping", "skydiving", "climbing", "cliff jumping",
    "bridge jump", "jump off a bridge", "jumping off a bridge", "diving",
    "swimming in deep water", "dare", "stunt",
]

OVERDOSE_MED_TERMS = [
    "pill", "pills", "medication", "medicine", "tablets", "painkillers",
    "sleeping pills", "antidepressants", "paracetamol", "acetaminophen",
    "ibuprofen", "opioids", "benzodiazepine", "xanax", "adderall",
]

TAKE_TERMS = ["take", "took", "drink", "drank", "swallow", "swallowed", "ingest", "ingested"]
SLEEP_AFTER_TERMS = ["go to bed", "sleep", "going to sleep", "see you tomorrow", "goodnight", "won't wake", "not wake"]
FRIEND_CONTEXT_TERMS = ["friends", "friend", "invited", "with them", "together", "group", "party"]
SUPERVISION_TERMS = ["instructor", "supervised", "company", "waiver", "harness", "equipment", "trained", "safety briefing"]
PRESSURE_FALLBACK_TERMS = [
    "if you cared", "if you loved me", "you owe me", "answer now", "right now",
    "don't tell anyone", "keep this secret", "or else", "prove it", "you have to",
    "you must", "no choice", "after all i've done", "everyone will know",
]


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def hits(text: str, terms: List[str]) -> List[str]:
    t = norm(text)
    return [term for term in terms if term in t]


def regex_any(text: str, patterns: List[str]) -> bool:
    t = norm(text)
    return any(re.search(pattern, t) for pattern in patterns)


def number_mentions(text: str) -> List[int]:
    nums: List[int] = []
    for match in re.finditer(r"\b(\d{1,3})\b", norm(text)):
        try:
            nums.append(int(match.group(1)))
        except ValueError:
            pass
    return nums


def severe_harm_context(text: str) -> Dict[str, object]:
    t = norm(text)
    nums = number_mentions(text)

    idiom = regex_any(text, DEATH_IDIOM_PATTERNS)
    self_harm = regex_any(text, SELF_HARM_INTENT_PATTERNS)

    med_hit = any(term in t for term in OVERDOSE_MED_TERMS)
    take_hit = any(term in t for term in TAKE_TERMS)
    sleep_hit = any(term in t for term in SLEEP_AFTER_TERMS)
    large_quantity = any(n >= 6 for n in nums)
    overdose_possible = med_hit and (take_hit or nums) and (large_quantity or sleep_hit)

    risk_activity = any(term in t for term in RISK_ACTIVITY_TERMS)
    friend_context = any(term in t for term in FRIEND_CONTEXT_TERMS)
    supervised_context = any(term in t for term in SUPERVISION_TERMS)
    pressure_hits = hits(text, PRESSURE_FALLBACK_TERMS)
    coercive_risk = risk_activity and bool(pressure_hits)

    context = "ordinary_social"
    reasons: List[str] = []
    death_possible = False
    urgency = "low"
    fail_closed = False

    if idiom and not self_harm and not overdose_possible:
        context = "expression_or_embarrassment"
        reasons.append("big wording looks like an expression")
    elif overdose_possible:
        context = "possible_overdose_or_poisoning"
        reasons.append("medication/pills plus risky amount or sleep-after context")
        death_possible = True
        urgency = "high"
        fail_closed = True
    elif self_harm:
        context = "possible_self_harm_or_immediate_danger"
        reasons.append("possible self-harm or immediate danger")
        death_possible = True
        urgency = "high"
        fail_closed = True
    elif coercive_risk:
        context = "risky_activity_with_pressure"
        reasons.append("risky activity plus pressure language")
        death_possible = True
        urgency = "medium"
    elif risk_activity:
        context = "recreational_or_physical_risk"
        reasons.append("risky activity")
        if friend_context:
            reasons.append("social/friend context")
        if supervised_context:
            reasons.append("supervision/equipment mentioned")
        death_possible = True
        urgency = "medium"
    elif any(word in t for word in ["die", "death", "dead", "kill"]):
        context = "big_words_unclear"
        reasons.append("big danger/death words are unclear")
        urgency = "medium"

    return {
        "context": context,
        "reasons": reasons,
        "death_possible": death_possible,
        "urgency": urgency,
        "fail_closed": fail_closed,
        "idiom_or_expression": idiom,
        "overdose_possible": overdose_possible,
        "self_harm_possible": self_harm,
        "risk_activity": risk_activity,
        "coercive_risk": coercive_risk,
    }


def safety_voice(severe: Dict[str, object]) -> str:
    context = severe["context"]
    if context == "possible_overdose_or_poisoning":
        return (
            "Hey, this worries me. Taking a lot of pills or medicine can be dangerous, especially before sleeping. "
            "Please don’t go to bed yet. Call poison control, emergency help, or someone near you now. "
            "I’d rather be too careful than miss something serious."
        )
    if context == "possible_self_harm_or_immediate_danger":
        return (
            "I’m really glad you said something. This sounds like real danger, not just a confusing moment. "
            "Please get help from emergency services or a trusted person near you right now. TechnBuddy is not enough for this alone."
        )
    if context == "recreational_or_physical_risk":
        return (
            "This sounds like a real activity that could be risky, not a self-harm message. "
            "Before you decide, check: do you want to do it, is it supervised, and is anyone making it hard to say no?"
        )
    if context == "risky_activity_with_pressure":
        return (
            "This sounds like a risky activity plus pressure from other people. You do not have to prove anything. "
            "You can ask safety questions, watch instead, or say no."
        )
    if context == "expression_or_embarrassment":
        return "Oof, that sounds really embarrassing. I’m reading that as a strong expression, not as danger."
    if context == "big_words_unclear":
        return (
            "I noticed strong words about danger or death. Sometimes people say that as an expression. "
            "Sometimes they mean real danger. Just to be safe: is this an expression, a risky activity, or real danger right now?"
        )
    return ""


def classify_quick_read(reading, severe: Dict[str, object]) -> str:
    context = severe["context"]
    if context == "possible_overdose_or_poisoning":
        return "get help now"
    if context == "possible_self_harm_or_immediate_danger":
        return "safety first"
    if context == "recreational_or_physical_risk":
        return "risk check"
    if context == "risky_activity_with_pressure":
        return "risk + boundary"
    if context == "expression_or_embarrassment":
        return "embarrassment / intensity"
    if context == "big_words_unclear":
        return "clarify danger"

    severities = {signal.severity for signal in reading.signals}
    keys = {signal.key for signal in reading.signals}
    if Severity.WARNING in severities:
        return "boundary warning"
    if "pressure" in keys:
        return "pressure signs"
    if "boundary" in keys:
        return "boundary check"
    if "evidence_gap" in keys:
        return "check evidence"
    if "repair_opportunity" in keys:
        return "repair opportunity"
    return "clear next step"


def signal_labels(reading) -> str:
    if not reading.signals:
        return "No obvious Sydney Protocol pressure signal detected."
    return ", ".join(signal.label for signal in reading.signals)


def matched_phrases(reading) -> List[str]:
    phrases = sorted({match for signal in reading.signals for match in signal.matches})
    return phrases[:8]


def zone_signals(reading) -> Dict[str, List[str]]:
    """Group core severities into TechnBuddy's simple signal zones.

    The zones are review aids only:
    - GREEN/INFO: helpful or repair-positive signals;
    - ORANGE/REVIEW: check-zone signals that need attention;
    - RED/WARNING: high-risk boundary signals.
    """
    zones = {"green": [], "orange": [], "red": []}
    for signal in reading.signals:
        item = f"**{signal.label}:** {signal.description}"
        if signal.severity == Severity.INFO:
            zones["green"].append(item)
        elif signal.severity == Severity.WARNING:
            zones["red"].append(item)
        else:
            zones["orange"].append(item)
    return zones


def default_zone_lines(zone: str) -> str:
    defaults = {
        "green": "No strong helpful signal was detected by the rule engine. Look for clear sender, clear reason, evidence, time to review, and a contact or appeal path.",
        "orange": "No check-zone signal was detected. Still review context before acting if the stakes are high.",
        "red": "No high-risk red flag was detected by the rule engine. This does not prove the message is safe or true.",
    }
    return defaults[zone]


def next_safe_step(reading, severe: Dict[str, object]) -> str:
    context = severe["context"]
    if context == "possible_overdose_or_poisoning":
        return "Do not wait or go to sleep. Contact emergency help, poison control, or someone near you now."
    if context == "possible_self_harm_or_immediate_danger":
        return "Get immediate help from emergency services or a trusted person near you. TechnBuddy is not enough for this alone."
    if context == "risky_activity_with_pressure":
        return "Pause before acting. Ask safety questions, remove the pressure, and choose only if you freely want to."
    if context == "recreational_or_physical_risk":
        return "Check supervision, equipment, consent, and whether anyone is making it hard to say no."

    severities = {signal.severity for signal in reading.signals}
    keys = {signal.key for signal in reading.signals}
    if Severity.WARNING in severities:
        return "Do not act on this blindly. Verify the sender, evidence, consequence, and review path through an independent channel."
    if "evidence_gap" in keys or "authority_overclaim" in keys:
        return "Ask what evidence, mechanism, authority, and review path support the claim before relying on it."
    if "pressure" in keys or "boundary" in keys:
        return "Slow the moment down. Ask for clarity, keep your option to say no, and avoid urgent action under pressure."
    if "repair_opportunity" in keys:
        return "Use the repair opening: ask one clear question, clarify the misunderstanding, or request a calmer next step."
    return "Read it once more, identify the requested action, and verify anything important before you act."


def build_reply(user_text: str, debug: bool = False) -> str:
    reading = analyze_text(user_text, profile="technbuddy_chat")
    receipt = create_receipt(reading)
    severe = severe_harm_context(user_text)
    warning = safety_voice(severe)
    quick_read = classify_quick_read(reading, severe)

    lines: List[str] = []
    if warning:
        lines.append(warning)
        lines.append("")

    lines.append("**TechnBuddy signal mirror**")
    lines.append(f"Quick read: **{quick_read}**")

    if severe["fail_closed"]:
        lines.append("")
        lines.append("**RED — High-risk factors**")
        lines.append("- Possible immediate danger. Treat this as safety first, not a normal message review.")
        lines.append("")
        lines.append("**Next safe step**")
        lines.append(next_safe_step(reading, severe))
        lines.append("")
        lines.append("**Your decision**")
        lines.append("TechnBuddy is not emergency help, therapy, a doctor, a lawyer, or an authority.")
        if debug:
            lines.append(f"\n`context={severe['context']}; receipt={receipt.receipt_id}; hash={reading.input_hash[:12]}`")
        return "\n".join(lines)

    zones = zone_signals(reading)

    lines.append("")
    lines.append("**GREEN — Helpful signals**")
    if zones["green"]:
        for item in zones["green"]:
            lines.append(f"- {item}")
    else:
        lines.append(f"- {default_zone_lines('green')}")

    lines.append("")
    lines.append("**ORANGE — Check zone**")
    if zones["orange"]:
        for item in zones["orange"]:
            lines.append(f"- {item}")
    else:
        lines.append(f"- {default_zone_lines('orange')}")

    lines.append("")
    lines.append("**RED — High-risk factors**")
    if zones["red"]:
        for item in zones["red"]:
            lines.append(f"- {item}")
    else:
        lines.append(f"- {default_zone_lines('red')}")

    lines.append("")
    lines.append("**Next safe step**")
    lines.append(next_safe_step(reading, severe))

    if reading.repair_questions:
        lines.append("")
        lines.append("**Questions before acting**")
        for question in reading.repair_questions[:3]:
            lines.append(f"- {question}")

    phrases = matched_phrases(reading)
    if phrases:
        lines.append("")
        lines.append("**Words that triggered review**")
        lines.append(", ".join(f"`{phrase}`" for phrase in phrases))

    lines.append("")
    lines.append("**Your decision**")
    lines.append("TechnBuddy shows signals before you act. It does not decide, certify, prove, or replace human review.")

    if debug:
        lines.append("")
        lines.append("**Protocol trace**")
        lines.append(f"- status: `{reading.status}`")
        lines.append(f"- profile: `{reading.profile}`")
        lines.append(f"- language: `{reading.language.value}`")
        lines.append(f"- receipt: `{receipt.receipt_id}`")
        lines.append(f"- input hash: `{reading.input_hash}`")
        lines.append(f"- signals: `{signal_labels(reading)}`")
        lines.append(f"- safety overlay context: `{severe['context']}`")

    return "\n".join(lines)


st.set_page_config(page_title="TechnBuddy", page_icon="🧭", layout="centered")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Cinzel:wght@600;700&display=swap');

    :root {
        --blue: #6689a4;
        --text: #4f5660;
        --muted: #7b8188;
        --border: rgba(127,159,183,0.25);
        --shadow: 0 10px 28px rgba(102, 137, 164, 0.10);
    }

    .stApp {
        background: radial-gradient(circle at top left, #fffdfb 0%, #f7f2ec 42%, #edf3f5 100%);
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }

    .block-container {
        padding-top: 1.25rem;
        max-width: 880px;
    }

    h1, h2, h3 {
        font-family: 'Cinzel', serif !important;
        color: var(--blue) !important;
    }

    p, div, span, label, li, strong, em { color: var(--text); }

    .tb-top {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.25rem;
        margin-bottom: 0.7rem;
    }

    .tb-title {
        font-family: 'Cinzel', serif;
        color: var(--blue);
        font-size: 2.0rem;
        font-weight: 700;
        margin-top: 0.35rem;
    }

    .tb-question {
        color: var(--text);
        font-size: 1.2rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.1rem;
    }

    .tb-sub {
        color: var(--muted);
        font-size: 0.98rem;
        text-align: center;
    }

    .tb-note {
        border: 1px solid var(--border);
        background: rgba(255,255,255,0.86);
        padding: 0.8rem 1rem;
        border-radius: 18px;
        margin: 0.55rem 0 0.55rem 0;
        box-shadow: 0 6px 18px rgba(102,137,164,0.08);
    }

    .tb-static-head {
        position: sticky;
        top: 0;
        z-index: 999;
        background: linear-gradient(180deg, rgba(255,253,251,0.98) 0%, rgba(247,242,236,0.95) 100%);
        backdrop-filter: blur(8px);
        padding-bottom: 0.25rem;
        border-bottom: 1px solid rgba(127,159,183,0.12);
    }

    .tb-chat-anchor {
        margin-top: 0.35rem;
        margin-bottom: 0.35rem;
    }

    [data-testid="stChatInput"] {
        position: sticky !important;
        bottom: 0 !important;
        z-index: 998 !important;
        background: linear-gradient(180deg, rgba(247,242,236,0.0), rgba(247,242,236,0.96) 35%) !important;
        padding-top: 0.5rem !important;
    }

    [data-testid="stChatInput"] textarea {
        background-color: #fffdfb !important;
        color: #4f5660 !important;
        border: 1px solid rgba(127,159,183,0.35) !important;
        border-radius: 16px !important;
    }

    .stButton > button {
        background: linear-gradient(180deg, #edf6f8 0%, #dfeef3 100%) !important;
        color: #506779 !important;
        border: 1px solid rgba(127,159,183,0.45) !important;
        border-radius: 14px !important;
        font-weight: 800 !important;
    }

    [data-testid="stExpander"] details {
        background: rgba(255,255,255,0.82);
        border: 1px solid rgba(127,159,183,0.18);
        border-radius: 16px;
        box-shadow: 0 6px 16px rgba(102,137,164,0.06);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.container():
    st.markdown('<div class="tb-static-head"><div class="tb-top">', unsafe_allow_html=True)
    if MASCOT_PATH.exists():
        st.image(str(MASCOT_PATH), width=245)
    st.markdown(
        """
            <div class="tb-title">TechnBuddy</div>
            <div class="tb-question">Green signals. Orange checks. Red flags. Your decision.</div>
            <div class="tb-sub">One input. One quick scan. No modules, no scores, no verdicts.</div>
        </div>
        <div class="tb-note">
            Paste a message, AI answer, email, form text, or situation. TechnBuddy groups bounded rule-based signals into <strong>GREEN</strong>, <strong>ORANGE</strong>, and <strong>RED</strong> before you act.
        </div>
        </div>
        <div class="tb-chat-anchor"></div>
        """,
        unsafe_allow_html=True,
    )

with st.expander("Tiny settings", expanded=False):
    st.session_state["debug"] = st.toggle(
        "Show review trace in replies",
        value=st.session_state.get("debug", False),
    )
    if st.button("Clear chat"):
        st.session_state["messages"] = []
        st.rerun()
    st.caption("TechnBuddy gives signals, not orders. The trace is for review, not authority.")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "assistant",
            "content": (
                "Hey, I’m TechnBuddy — a quick signal mirror. "
                "Paste a message, AI answer, email, form text, or situation. I’ll show GREEN helpful signals, ORANGE checks, RED flags, and one safer next step."
            ),
        }
    ]

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"], avatar="🧭" if msg["role"] == "assistant" else "🙂"):
        st.markdown(msg["content"])

prompt = st.chat_input("Paste a message, AI answer, email, form text, or situation...", key="technbuddy_main_chat_input")
if prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    reply = build_reply(prompt, debug=st.session_state.get("debug", False))
    st.session_state["messages"].append({"role": "assistant", "content": reply})
    st.rerun()

with st.expander("How TechnBuddy works", expanded=False):
    st.markdown(
        """
        TechnBuddy is a quick signal mirror wired to the **Sydney Protocol Core**.

        It stays intentionally simple: one input, no module router, no scores, no verdicts, no certification, and no LLM required for the core scan.

        It groups bounded review signals into:

        - **GREEN** — helpful or repair-positive signals;
        - **ORANGE** — check-zone signals that need attention;
        - **RED** — high-risk boundary signals.

        The Sydney Protocol Core does **not** decide what is true, illegal, corrupt, safe, or legitimate. It surfaces bounded review signals and repair questions for human judgment.
        """
    )
    st.markdown(
        """
        **TechnBuddy Promise**

        - I show signals, not orders.
        - I do not decide what someone definitely meant.
        - I separate helpful signals, check-zone signals, and high-risk factors.
        - I notice pressure, guilt, control, evidence gaps, and no-room-to-say-no moments.
        - I help protect boundaries, safety, dignity, and repair.
        - I switch to safety-first language if danger may be present.
        - I never make the app, a person, or a social rule the final authority.
        """
    )

st.caption(f"{APP_VERSION} · Green/Orange/Red signal mirror · not a therapist, judge, doctor, lawyer, emergency service, or authority")
