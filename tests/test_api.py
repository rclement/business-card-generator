import mimetypes

from http import HTTPStatus
from faker import Faker
from fastapi.testclient import TestClient


def test_get_card_success(app_client: TestClient, faker: Faker) -> None:
    params = dict(name=faker.name())

    response = app_client.get("/api/card", params=params)

    assert response.status_code == HTTPStatus.OK
    assert response.headers["content-type"] == mimetypes.types_map[".svg"]
    assert response.text.startswith('<?xml version="1.0" encoding="utf-8"?>\n<svg')
    assert response.text.endswith("</svg>\n")


def test_get_card_format_png(app_client: TestClient, faker: Faker) -> None:
    params = dict(name=faker.name(), format="png")

    response = app_client.get("/api/card", params=params)

    assert response.status_code == HTTPStatus.OK
    assert response.headers["content-type"] == mimetypes.types_map[".png"]
    assert len(response.content) > 0
