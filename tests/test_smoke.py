"""Basic smoke test for the project."""

from src.job_agent.main import main


def test_main_is_callable() -> None:
    assert callable(main)
