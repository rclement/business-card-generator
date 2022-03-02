from business_card_generator import settings


def test_load_valid() -> None:
    s = settings.Settings()

    assert s.app_name
    assert s.app_description
    assert s.app_version
    assert s.app_environment == "testing"
