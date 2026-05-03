"""Eval-specific fixtures + CLI flag for baseline updates."""

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--update-baselines", action="store_true", default=False,
        help="Update tests/evals/_baseline_scores.json with current scores",
    )


@pytest.fixture
def update_baselines(request) -> bool:
    return request.config.getoption("--update-baselines")
