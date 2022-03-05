from http import HTTPStatus
from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_get_home_success(app: FastAPI, app_client: TestClient) -> None:
    from business_card_generator import __about__

    response = app_client.get("/")
    assert response.status_code == HTTPStatus.OK

    data = response.text
    assert __about__.__name__ in data
    assert __about__.__version__ in data
    assert __about__.__description__ in data
    assert app.url_path_for("swagger_ui_html") in data
    assert app.url_path_for("redoc_html") in data
