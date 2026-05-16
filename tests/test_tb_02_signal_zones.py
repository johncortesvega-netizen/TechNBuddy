from sydney_protocol_core import analyze_text
from sydney_protocol_core.models import Severity


def test_core_severity_values_map_to_technbuddy_zones():
    mapping = {
        Severity.INFO: "GREEN",
        Severity.REVIEW: "ORANGE",
        Severity.WARNING: "RED",
    }

    assert mapping[Severity.INFO] == "GREEN"
    assert mapping[Severity.REVIEW] == "ORANGE"
    assert mapping[Severity.WARNING] == "RED"


def test_review_signal_maps_to_orange_zone():
    reading = analyze_text("You must do this right now and ask no questions.", profile="technbuddy_chat")

    assert any(signal.severity == Severity.REVIEW for signal in reading.signals)


def test_warning_signal_maps_to_red_zone():
    reading = analyze_text("This is the final decision. No objection is allowed.", profile="technbuddy_chat")

    assert any(signal.severity == Severity.WARNING for signal in reading.signals)


def test_repair_opportunity_can_supply_green_signal():
    reading = analyze_text("Sorry for the misunderstanding, can we clarify and review this?", profile="technbuddy_chat")

    assert any(signal.severity == Severity.INFO for signal in reading.signals)
