from business_card_generator import wsgi


def test_app_success() -> None:
    assert wsgi.app
