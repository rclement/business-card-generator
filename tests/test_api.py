import mimetypes
import pytest

from http import HTTPStatus
from typing import Any, Dict
from fastapi.testclient import TestClient


def test_get_vcard_svg_success(
    app_client: TestClient, card_params: Dict[str, str]
) -> None:
    response = app_client.get("/api/vcard.svg", params=card_params)

    assert response.status_code == HTTPStatus.OK
    assert response.headers["content-type"] == mimetypes.types_map[".svg"]
    assert response.headers["content-disposition"] == "filename=vcard.svg"
    assert len(response.content) > 0
    assert response.text.startswith(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg"'
        ' width="164.0" height="164.0" class="vcard">'
    )
    assert response.text.endswith("</svg>\n")


@pytest.mark.parametrize(
    ("key", "value"),
    (
        ("birthday", "unknown"),
        ("email", "aaa@bbb"),
    ),
)
def test_get_vcard_svg_invalid_parameter(
    app_client: TestClient, card_params: Dict[str, str], key: str, value: Any
) -> None:
    card_params[key] = value

    response = app_client.get("/api/vcard.svg", params=card_params)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


# ------------------------------------------------------------------------------


def test_get_vcard_png_success(
    app_client: TestClient, card_params: Dict[str, str]
) -> None:
    response = app_client.get("/api/vcard.png", params=card_params)

    assert response.status_code == HTTPStatus.OK
    assert response.headers["content-type"] == mimetypes.types_map[".png"]
    assert response.headers["content-disposition"] == "filename=vcard.png"
    assert len(response.content) > 0


# ------------------------------------------------------------------------------


def test_get_vcard_vcf_success(
    app_client: TestClient, card_params: Dict[str, str]
) -> None:
    response = app_client.get("/api/vcard.vcf", params=card_params)

    assert response.status_code == HTTPStatus.OK
    assert (
        response.headers["content-type"]
        == f'{mimetypes.types_map[".vcf"]}; charset=utf-8'
    )
    assert response.headers["content-disposition"] == "filename=vcard.vcf"
    assert len(response.content) > 0
    assert (
        response.text == "BEGIN:VCARD\r\n"
        "VERSION:3.0\r\n"
        f'N:{card_params["name"]}\r\n'
        f'FN:{card_params["name"]}\r\n'
        "END:VCARD\r\n"
    )


# ------------------------------------------------------------------------------


def test_get_mecard_svg_success(
    app_client: TestClient, card_params: Dict[str, str]
) -> None:
    response = app_client.get("/api/mecard.svg", params=card_params)

    assert response.status_code == HTTPStatus.OK
    assert response.headers["content-type"] == mimetypes.types_map[".svg"]
    assert response.headers["content-disposition"] == "filename=mecard.svg"
    assert len(response.content) > 0
    assert response.text.startswith(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg"'
        ' width="132.0" height="132.0" class="mecard">'
    )
    assert response.text.endswith("</svg>\n")


# ------------------------------------------------------------------------------


def test_get_mecard_png_success(
    app_client: TestClient, card_params: Dict[str, str]
) -> None:
    response = app_client.get("/api/mecard.png", params=card_params)

    assert response.status_code == HTTPStatus.OK
    assert response.headers["content-type"] == mimetypes.types_map[".png"]
    assert response.headers["content-disposition"] == "filename=mecard.png"
    assert len(response.content) > 0


# ------------------------------------------------------------------------------


def test_get_mecard_vcf_success(
    app_client: TestClient, card_params: Dict[str, str]
) -> None:
    response = app_client.get("/api/mecard.vcf", params=card_params)

    assert response.status_code == HTTPStatus.OK
    assert (
        response.headers["content-type"]
        == f'{mimetypes.types_map[".vcf"]}; charset=utf-8'
    )
    assert response.headers["content-disposition"] == "filename=mecard.vcf"
    assert len(response.content) > 0
    assert response.text == f'MECARD:N:{card_params["name"]};;'
