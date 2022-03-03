from business_card_generator import asgi


def test_app_success() -> None:
    assert asgi.app
