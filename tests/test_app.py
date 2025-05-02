import mimetypes
import pytest

from datetime import date
from http import HTTPStatus
from typing import Any, Dict
from flask import Flask, url_for
from flask.testing import FlaskClient


# ------------------------------------------------------------------------------


@pytest.fixture(scope="function")
def enable_force_https(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FORCE_HTTPS", "true")


# ------------------------------------------------------------------------------


def test_get_home_https_redirect(
    enable_force_https: None, app_client: FlaskClient
) -> None:
    response = app_client.get("/", follow_redirects=False)
    assert response.status_code == HTTPStatus.FOUND
    assert response.location.startswith("https://")


def test_get_home_success(app: Flask, app_client: FlaskClient) -> None:
    from business_card_generator import __about__

    response = app_client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.mimetype == "text/html"

    data = response.get_data().decode("utf-8")
    assert __about__.__name__ in data
    assert __about__.__version__ in data
    assert __about__.__description__ in data

    assert '<form method="GET"' in data
    assert url_for("views.get_card") in data

    assert "Card Type" in data
    assert "vCard" in data
    assert "MeCard" in data

    assert "Profile" in data
    assert "First Name" in data
    assert "Last Name" in data
    assert "Nickname" in data
    assert "Picture URL" in data
    assert "Birthday" in data

    assert "Organization" in data
    assert "Company" in data
    assert "Job" in data
    assert "Email" in data
    assert "Phone" in data
    assert "Website" in data

    assert "Address" in data
    assert "Street" in data
    assert "City" in data
    assert "Zipcode" in data
    assert "State" in data
    assert "Country" in data
    assert "Generate" in data


@pytest.mark.parametrize("card_type", (("vcard", "mecard")))
def test_get_home_with_params(
    app: Flask,
    app_client: FlaskClient,
    card_params: Dict[str, str],
    card_type: str,
) -> None:
    params = dict(
        card_type=card_type,
        **card_params,
    )

    response = app_client.get("/", query_string=params)
    assert response.status_code == HTTPStatus.OK
    assert response.mimetype == "text/html"

    data = response.get_data().decode("utf-8")

    assert f'value="{params["card_type"]}" checked' in data
    for v in card_params.values():
        assert v in data


@pytest.mark.parametrize("card_type", (("vcard", "mecard")))
def test_get_card_success(
    app: Flask,
    app_client: FlaskClient,
    card_params: Dict[str, str],
    card_type: str,
) -> None:
    params = dict(
        card_type=card_type,
        **card_params,
    )

    response = app_client.get("/card", query_string=params)
    assert response.status_code == HTTPStatus.OK
    assert response.mimetype == "text/html"

    data = response.get_data().decode("utf-8")

    assert "<img src=" in data
    assert url_for(f"views.get_{card_type}_svg") in data

    assert "Edit" in data
    assert url_for("views.get_home") in data

    assert "PNG" in data
    assert url_for(f"views.get_{card_type}_png") in data

    assert "VCF" in data
    assert url_for(f"views.get_{card_type}_vcf") in data

    for v in card_params.values():
        assert v in data


# ------------------------------------------------------------------------------


def test_get_vcard_svg_success(
    app_client: FlaskClient, card_params: Dict[str, str]
) -> None:
    response = app_client.get("/vcard.svg", query_string=card_params)

    assert response.status_code == HTTPStatus.OK
    assert (
        response.headers["content-type"]
        == f"{mimetypes.types_map['.svg']}; charset=utf-8"
    )
    assert response.headers["content-disposition"] == "inline; filename=vcard.svg"

    data = response.get_data().decode("utf-8")
    assert len(data) > 0
    assert data.startswith(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg"'
        ' width="292.0" height="292.0" class="vcard">'
    )
    assert data.endswith("</svg>\n")


@pytest.mark.parametrize(
    "param",
    (
        "nickname",
        "birthday",
        "company",
        "job",
        "email",
        "phone",
        "website",
        "picture",
        "street",
        "city",
        "zipcode",
        "state",
        "country",
    ),
)
def test_get_vcard_svg_optional_empty_parameter(
    app_client: FlaskClient, card_params: Dict[str, str], param: str
) -> None:
    card_params[param] = ""
    response = app_client.get("/vcard.svg", query_string=card_params)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    ("key", "value"),
    (
        ("birthday", "unknown"),
        ("email", "aaa@bbb"),
    ),
)
def test_get_vcard_svg_invalid_parameter(
    app_client: FlaskClient, card_params: Dict[str, str], key: str, value: Any
) -> None:
    card_params[key] = value
    response = app_client.get("/vcard.svg", query_string=card_params)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


# ------------------------------------------------------------------------------


def test_get_vcard_png_success(
    app_client: FlaskClient, card_params: Dict[str, str]
) -> None:
    response = app_client.get("/vcard.png", query_string=card_params)

    assert response.status_code == HTTPStatus.OK
    assert response.headers["content-type"] == mimetypes.types_map[".png"]
    assert response.headers["content-disposition"] == "inline; filename=vcard.png"
    assert len(response.get_data()) > 0


# ------------------------------------------------------------------------------


def test_get_vcard_vcf_success(
    app_client: FlaskClient, card_params: Dict[str, str]
) -> None:
    response = app_client.get("/vcard.vcf", query_string=card_params)

    assert response.status_code == HTTPStatus.OK
    assert (
        response.headers["content-type"]
        == f"{mimetypes.types_map['.vcf']}; charset=utf-8"
    )
    assert response.headers["content-disposition"] == "inline; filename=vcard.vcf"

    company = card_params["company"].replace(",", "\\,")
    data = response.get_data().decode("utf-8")
    assert len(data) > 0
    assert (
        data == "BEGIN:VCARD\r\n"
        "VERSION:3.0\r\n"
        f"N:{card_params['lastname']};{card_params['firstname']}\r\n"
        f"FN:{card_params['firstname']} {card_params['lastname']}\r\n"
        f"ORG:{company}\r\n"
        f"EMAIL:{card_params['email']}\r\n"
        f"TEL:{card_params['phone']}\r\n"
        f"URL:{card_params['website']}\r\n"
        f"TITLE:{card_params['job']}\r\n"
        f"PHOTO;VALUE=uri:{card_params['picture']}\r\n"
        f"NICKNAME:{card_params['nickname']}\r\n"
        f"ADR:;;{card_params['street']};"
        f"{card_params['city']};"
        f"{card_params['state']};"
        f"{card_params['zipcode']};"
        f"{card_params['country']}\r\n"
        f"BDAY:{card_params['birthday']}\r\n"
        "END:VCARD\r\n"
    )


# ------------------------------------------------------------------------------


def test_get_mecard_svg_success(
    app_client: FlaskClient, card_params: Dict[str, str]
) -> None:
    response = app_client.get("/mecard.svg", query_string=card_params)

    assert response.status_code == HTTPStatus.OK
    assert (
        response.headers["content-type"]
        == f"{mimetypes.types_map['.svg']}; charset=utf-8"
    )
    assert response.headers["content-disposition"] == "inline; filename=mecard.svg"

    data = response.get_data().decode("utf-8")
    assert len(data) > 0
    assert data.startswith(
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg"'
        ' width="244.0" height="244.0" class="mecard">'
    )
    assert data.endswith("</svg>\n")


# ------------------------------------------------------------------------------


def test_get_mecard_png_success(
    app_client: FlaskClient, card_params: Dict[str, str]
) -> None:
    response = app_client.get("/mecard.png", query_string=card_params)

    assert response.status_code == HTTPStatus.OK
    assert response.headers["content-type"] == mimetypes.types_map[".png"]
    assert response.headers["content-disposition"] == "inline; filename=mecard.png"
    assert len(response.get_data()) > 0


# ------------------------------------------------------------------------------


def test_get_mecard_vcf_success(
    app_client: FlaskClient, card_params: Dict[str, str]
) -> None:
    response = app_client.get("/mecard.vcf", query_string=card_params)

    assert response.status_code == HTTPStatus.OK
    assert (
        response.headers["content-type"]
        == f"{mimetypes.types_map['.vcf']}; charset=utf-8"
    )
    assert response.headers["content-disposition"] == "inline; filename=mecard.vcf"

    website = card_params["website"].replace(":", "\\:")
    data = response.get_data().decode("utf-8")
    assert len(data) > 0
    assert (
        data == f"MECARD:N:{card_params['lastname']},{card_params['firstname']};"
        f"TEL:{card_params['phone']};"
        f"EMAIL:{card_params['email']};"
        f"NICKNAME:{card_params['nickname']};"
        f"BDAY:{date.fromisoformat(card_params['birthday']).strftime('%Y%m%d')};"
        f"URL:{website};"
        f"ADR:,,{card_params['street']},"
        f"{card_params['city']},"
        f"{card_params['state']},"
        f"{card_params['zipcode']},"
        f"{card_params['country']};"
        f"MEMO:{card_params['company']};"
        ";"
    )
