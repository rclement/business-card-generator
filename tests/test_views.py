from http import HTTPStatus
from typing import Dict
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest


def test_get_home_success(app: FastAPI, app_client: TestClient) -> None:
    from business_card_generator import __about__

    response = app_client.get("/")
    assert response.status_code == HTTPStatus.OK

    data = response.text
    assert __about__.__name__ in data
    assert __about__.__version__ in data
    assert __about__.__description__ in data

    assert "API Documentation" in data
    assert app.url_path_for("swagger_ui_html") in data
    assert app.url_path_for("redoc_html") in data

    assert '<form method="GET"' in data
    assert app.url_path_for("get_card") in data

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
    app: FastAPI,
    app_client: TestClient,
    card_params: Dict[str, str],
    card_type: str,
) -> None:
    params = dict(
        card_type=card_type,
        **card_params,
    )

    response = app_client.get("/", params=params)
    assert response.status_code == HTTPStatus.OK

    data = response.text

    assert f'value="{params["card_type"]}" checked' in data
    for v in card_params.values():
        assert v in data


@pytest.mark.parametrize("card_type", (("vcard", "mecard")))
def test_get_card_success(
    app: FastAPI,
    app_client: TestClient,
    card_params: Dict[str, str],
    card_type: str,
) -> None:
    params = dict(
        card_type=card_type,
        **card_params,
    )

    response = app_client.get("/card", params=params)
    assert response.status_code == HTTPStatus.OK

    data = response.text

    assert "<img src=" in data
    assert app.url_path_for(f"get_{card_type}_svg") in data

    assert "Edit" in data
    assert app.url_path_for("get_home") in data

    assert "Download" in data
    assert app.url_path_for(f"get_{card_type}_vcf") in data

    # for v in card_params.values():
    #     assert v in data
