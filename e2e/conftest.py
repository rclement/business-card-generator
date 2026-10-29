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
    headers = {"User-Agent": "bcg-e2e"}
    # Only needed when the target is behind Vercel deployment protection
    bypass = os.environ.get("VERCEL_AUTOMATION_BYPASS_SECRET")
    if bypass:
        headers["x-vercel-protection-bypass"] = bypass

    with httpx2.Client(
        base_url=base_url, headers=headers, timeout=30, follow_redirects=False
    ) as http:
        # wait for the deployment (or alias) to serve the app
        for _ in range(30):
            try:
                if http.get("/", follow_redirects=True).status_code == 200:
                    break
            except httpx2.TransportError:
                pass
            time.sleep(5)
        else:
            pytest.exit(f"{base_url} is not ready", returncode=2)
        yield http
