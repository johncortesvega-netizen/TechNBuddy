from pathlib import Path

from sydney_protocol_core import analyze_text, create_receipt

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / "app.py").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")


def test_core_profile_detects_pressure():
    reading = analyze_text("You must answer right now and do not question this.", profile="technbuddy_chat")
    keys = {signal.key for signal in reading.signals}
    assert "pressure" in keys
    assert reading.profile == "technbuddy_chat"
    assert "not_authority" in {note.key for note in reading.boundary_notes}


def test_receipt_is_trace_not_certification():
    reading = analyze_text("Only we can make the final decision. No appeal.", profile="technbuddy_chat")
    receipt = create_receipt(reading).to_dict()
    assert receipt["receipt_id"].startswith("spr_")
    assert "not certification" in receipt["non_throne_statement"].lower()
    assert receipt["input_hash"] == reading.input_hash


def test_app_uses_core_and_keeps_one_input_posture():
    assert "from sydney_protocol_core import analyze_text, create_receipt" in APP
    assert 'profile="technbuddy_chat"' in APP
    assert "Green signals. Orange checks. Red flags. Your decision." in APP
    assert "No module router" in README
    assert "No scores" in README


def test_no_embedded_base64_mascot_constant():
    assert "MASCOT_B64" not in APP
    assert "assets/technbuddy_mascot.png" in README or "technbuddy_mascot.png" in APP
