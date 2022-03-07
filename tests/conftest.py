import os
import pytest

from typing import Dict, Generator
from faker import Faker
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


@pytest.fixture(scope="function")
def card_params(faker: Faker) -> Dict[str, str]:
    return dict(name=faker.name())
