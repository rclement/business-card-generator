import re
from http import HTTPStatus

import httpx
import pytest

CARD_TYPES = ["vcard", "mecard"]
CARD_PARAMS = {
    "firstname": "Ada",
    "lastname": "Lovelace",
    "company": "Analytical Engines",
    "email": "ada@example.com",
    "website": "https://example.com/",
}
# (format, content type, bytes expected near the start of the body)
CARD_FORMATS = [
    ("svg", "image/svg+xml", b"<svg"),
    ("png", "image/png", b"\x89PNG"),
    ("vcf", "text/", b""),
]

pytestmark = pytest.mark.e2e


def test_home(client: httpx.Client) -> None:
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert "text/html" in response.headers["content-type"]
    assert "<form" in response.text


def test_static_assets(client: httpx.Client) -> None:
    match = re.search(r'(?:href|src)="(/static/[^"]+)"', client.get("/").text)
    assert match
    assert client.get(match.group(1)).status_code == HTTPStatus.OK


@pytest.mark.parametrize("card_type", CARD_TYPES)
def test_form_flow(client: httpx.Client, card_type: str) -> None:
    response = client.post("/", data={"card_type": card_type, **CARD_PARAMS})
    assert response.status_code == HTTPStatus.FOUND

    location = response.headers["location"]
    assert f"/card?card_type={card_type}" in location
    assert client.get(location).status_code == HTTPStatus.OK


def test_form_validation(client: httpx.Client) -> None:
    response = client.post("/", data={"card_type": "vcard", "firstname": "Ada"})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("card_type", CARD_TYPES)
@pytest.mark.parametrize(("card_format", "content_type", "prefix"), CARD_FORMATS)
def test_card_output(
    client: httpx.Client,
    card_type: str,
    card_format: str,
    content_type: str,
    prefix: bytes,
) -> None:
    response = client.get(f"/{card_type}.{card_format}", params=CARD_PARAMS)
    assert response.status_code == HTTPStatus.OK
    assert content_type in response.headers["content-type"]
    assert prefix in response.content[:200]
    if card_format == "vcf":
        assert b"Lovelace" in response.content


@pytest.mark.parametrize("card_type", CARD_TYPES)
@pytest.mark.parametrize("card_format", [f for f, _, _ in CARD_FORMATS])
def test_card_output_invalid(
    client: httpx.Client, card_type: str, card_format: str
) -> None:
    response = client.get(f"/{card_type}.{card_format}", params={"firstname": "Ada"})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
