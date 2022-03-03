import mimetypes
import pytest

from http import HTTPStatus
from typing import Any
from faker import Faker
from fastapi.testclient import TestClient


@pytest.mark.parametrize("kind", (None, "mecard", "vcard"))
def test_get_card_success(app_client: TestClient, faker: Faker, kind: str) -> None:
    params = dict(name=faker.name(), kind=kind)

    response = app_client.get("/api/card", params=params)

    assert response.status_code == HTTPStatus.OK
    assert response.headers["content-type"] == mimetypes.types_map[".svg"]
    assert len(response.content) > 0
    assert response.text.startswith('<?xml version="1.0" encoding="utf-8"?>\n<svg')
    assert response.text.endswith("</svg>\n")


@pytest.mark.parametrize("kind", (None, "mecard", "vcard"))
def test_get_card_format_png(app_client: TestClient, faker: Faker, kind: str) -> None:
    params = dict(name=faker.name(), format="png", kind=kind)

    response = app_client.get("/api/card", params=params)

    assert response.status_code == HTTPStatus.OK
    assert response.headers["content-type"] == mimetypes.types_map[".png"]
    assert len(response.content) > 0


@pytest.mark.parametrize(
    ("key", "value"),
    (
        ("kind", "unknown"),
        ("format", "unknown"),
        ("scale", "unknown"),
        ("birthday", "unknown"),
        ("email", "aaa@bbb"),
    ),
)
def test_get_card_invalid_parameter(
    app_client: TestClient, faker: Faker, key: str, value: Any
) -> None:
    params = {"name": faker.name(), key: value}

    response = app_client.get("/api/card", params=params)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
