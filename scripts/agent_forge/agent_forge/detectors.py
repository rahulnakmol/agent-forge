"""Consolidated CLI detection across all registered translators."""

from agent_forge.translators import get_translator, registered_translators


def detect_all_clis() -> dict[str, bool]:
    """Return {cli_name: detected_on_this_machine}."""
    result: dict[str, bool] = {}
    for name in registered_translators():
        translator = get_translator(name)
        if translator.tier == "3":
            continue  # Tier 3 (prompt_loader) has no detection
        try:
            result[name] = bool(translator.detect())
        except Exception:
            result[name] = False
    return result
