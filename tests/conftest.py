import os
import pytest

from typing import Dict, Generator
from faker import Faker
from flask import Flask
from flask.testing import FlaskClient


# ------------------------------------------------------------------------------


os.environ["APP_ENVIRONMENT"] = "testing"
os.environ["FORCE_HTTPS"] = "false"


# ------------------------------------------------------------------------------


@pytest.fixture(scope="function")
def app() -> Generator[Flask, None, None]:
    from business_card_generator.app import create_app

    yield create_app(None)


@pytest.fixture(scope="function")
def app_client(app: Flask) -> Generator[FlaskClient, None, None]:
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="function")
def card_params(faker: Faker) -> Dict[str, str]:
    return dict(
        firstname=faker.first_name(),
        lastname=faker.last_name(),
        nickname=faker.first_name(),
        birthday=faker.date(),
        company=faker.company(),
        job=faker.job(),
        email=faker.email(),
        phone=faker.phone_number(),
        website=faker.url(),
        picture=faker.image_url(),
        street=faker.street_address(),
        city=faker.city(),
        zipcode=faker.zipcode(),
        state=faker.state(),
        country=faker.country(),
    )
