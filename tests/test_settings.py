import json
import os
import pytest

from business_card_generator import settings


def test_load_env() -> None:
    s = settings.Settings()

    assert s.app_environment == os.getenv("APP_ENVIRONMENT")
    assert s.force_https == json.loads(os.getenv("FORCE_HTTPS", ""))


def test_load_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("APP_ENVIRONMENT")
    monkeypatch.delenv("FORCE_HTTPS")

    s = settings.Settings()

    assert s.app_environment == "production"
    assert s.force_https
