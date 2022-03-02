import pytest

from http import HTTPStatus
from fastapi import FastAPI
from fastapi.testclient import TestClient


# ------------------------------------------------------------------------------


@pytest.fixture(scope="function")
def enable_force_https(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FORCE_HTTPS", "true")


# ------------------------------------------------------------------------------


def test_app_urls(app: FastAPI) -> None:
    assert app.url_path_for("openapi") == "/openapi.json"
    assert app.url_path_for("swagger_ui_html") == "/docs"
    assert app.url_path_for("redoc_html") == "/redoc"


# ------------------------------------------------------------------------------


def test_get_docs_https_redirect(
    enable_force_https: None, app_client: TestClient
) -> None:
    response = app_client.get("/docs", allow_redirects=False)
    assert response.status_code == HTTPStatus.TEMPORARY_REDIRECT
    assert response.headers["location"].startswith("https://")
