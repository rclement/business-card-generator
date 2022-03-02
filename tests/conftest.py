import os
import pytest

from typing import Generator
from fastapi import FastAPI
from fastapi.testclient import TestClient


# ------------------------------------------------------------------------------


os.environ["APP_ENVIRONMENT"] = "testing"
os.environ["FORCE_HTTPS"] = "false"


# ------------------------------------------------------------------------------


@pytest.fixture(scope="function")
def app() -> FastAPI:
    from business_card_generator.app import create_app

    return create_app(None)


@pytest.fixture(scope="function")
def app_client(app: FastAPI) -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client
