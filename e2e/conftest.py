import os
import time
from collections.abc import Iterator

import httpx2
import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--base-url",
        default=os.environ.get("E2E_BASE_URL"),
        help="Base URL of the running instance to test (or set E2E_BASE_URL)",
    )


@pytest.fixture(scope="session")
def base_url(request: pytest.FixtureRequest) -> str:
    url = request.config.getoption("--base-url")
    if not url:
        pytest.exit("--base-url (or E2E_BASE_URL) is required", returncode=2)
    return str(url).rstrip("/")


@pytest.fixture(scope="session")
def client(base_url: str) -> Iterator[httpx2.Client]:
    with httpx2.Client(
        base_url=base_url,
        headers={"User-Agent": "bcg-e2e"},
        timeout=30,
        follow_redirects=False,
    ) as http:
        # wait for the deployment (or alias) to serve the app
        last: str = "no response"
        for _ in range(30):
            try:
                status = http.get("/", follow_redirects=True).status_code
                if status == 200:
                    break
                last = f"HTTP {status}"
            except httpx2.TransportError as exc:
                last = repr(exc)
            time.sleep(5)
        else:
            pytest.exit(f"{base_url} is not ready (last: {last})", returncode=2)
        yield http
