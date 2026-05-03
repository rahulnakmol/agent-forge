"""tests/unit/test_detectors.py"""

from agent_forge.detectors import detect_all_clis


def test_returns_dict_of_translator_to_bool() -> None:
    detected = detect_all_clis()
    expected_keys = {
        "claude-code", "copilot-cli", "codex-cli", "cursor",
        "amp", "gemini-cli", "kilocode", "opencode", "crush",
    }
    assert set(detected.keys()) >= expected_keys
    # All values are booleans
    assert all(isinstance(v, bool) for v in detected.values())
