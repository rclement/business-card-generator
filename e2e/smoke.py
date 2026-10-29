"""End-to-end smoke tests against a running instance (local container or preview).

Usage: python e2e/smoke.py BASE_URL

Standard library only, so it can run anywhere without installing dependencies.
Set VERCEL_AUTOMATION_BYPASS_SECRET if the target is behind Vercel deployment protection.
"""

import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable
from http import HTTPStatus

PARAMS = {
    "firstname": "Ada",
    "lastname": "Lovelace",
    "company": "Analytical Engines",
    "email": "ada@example.com",
    "website": "https://example.com/",
}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        return None


def request(
    base_url: str,
    path: str,
    data: dict[str, str] | None = None,
    follow_redirects: bool = True,
) -> tuple[int, dict[str, str], bytes]:
    headers = {"User-Agent": "bcg-e2e-smoke"}
    bypass = os.environ.get("VERCEL_AUTOMATION_BYPASS_SECRET")
    if bypass:
        headers["x-vercel-protection-bypass"] = bypass
    body = urllib.parse.urlencode(data).encode() if data is not None else None
    req = urllib.request.Request(base_url + path, data=body, headers=headers)
    handlers = [] if follow_redirects else [NoRedirect()]
    opener = urllib.request.build_opener(*handlers)
    try:
        with opener.open(req, timeout=30) as resp:
            return resp.status, dict(resp.headers), resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, dict(exc.headers), exc.read()


def wait_until_ready(base_url: str, attempts: int = 30, delay: float = 5.0) -> None:
    """Wait for the deployment (or alias) to serve the app."""
    for _ in range(attempts):
        try:
            status, _, _ = request(base_url, "/")
            if status == HTTPStatus.OK:
                return
        except OSError:
            pass
        time.sleep(delay)
    raise SystemExit(f"{base_url} not ready after {attempts} attempts")


def check(cond: bool, message: str) -> None:
    if not cond:
        raise AssertionError(message)


def test_home(base_url: str) -> None:
    status, headers, body = request(base_url, "/")
    check(status == HTTPStatus.OK, f"GET / -> {status}")
    check("text/html" in headers.get("Content-Type", ""), "home is not html")
    check(b"<form" in body, "home has no form")


def test_static(base_url: str) -> None:
    _, _, body = request(base_url, "/")
    import re

    match = re.search(rb'(?:href|src)="(/static/[^"]+)"', body)
    check(match is not None, "no static asset referenced in home")
    assert match is not None
    status, _, _ = request(base_url, match.group(1).decode())
    check(status == HTTPStatus.OK, f"static asset -> {status}")


def test_form_flow(base_url: str) -> None:
    for card_type in ("vcard", "mecard"):
        status, headers, _ = request(
            base_url,
            "/",
            data={"card_type": card_type, **PARAMS},
            follow_redirects=False,
        )
        check(status == HTTPStatus.FOUND, f"POST {card_type} -> {status}")
        location = headers.get("Location", "")
        check("/card" in location and card_type in location, f"bad redirect {location}")
        status, _, body = request(
            base_url,
            urllib.parse.urlparse(location).path
            + "?"
            + urllib.parse.urlparse(location).query,
        )
        check(status == HTTPStatus.OK, f"GET {location} -> {status}")


def test_form_validation(base_url: str) -> None:
    status, _, _ = request(base_url, "/", data={"card_type": "vcard", "firstname": "x"})
    check(status == HTTPStatus.UNPROCESSABLE_ENTITY, f"invalid POST -> {status}")


def test_card_outputs(base_url: str) -> None:
    query = "?" + urllib.parse.urlencode(PARAMS)
    expected = {
        "vcard.svg": (b"<svg", "image/svg+xml"),
        "vcard.png": (b"\x89PNG", "image/png"),
        "vcard.vcf": (b"BEGIN:VCARD", "text/"),
        "mecard.svg": (b"<svg", "image/svg+xml"),
        "mecard.png": (b"\x89PNG", "image/png"),
        "mecard.vcf": (b"MECARD:", "text/"),
    }
    for name, (magic, mimetype) in expected.items():
        status, headers, body = request(base_url, f"/{name}{query}")
        check(status == HTTPStatus.OK, f"GET {name} -> {status}")
        check(mimetype in headers.get("Content-Type", ""), f"{name} mimetype")
        check(magic in body[:200], f"{name} content does not start with {magic!r}")
        check(b"Lovelace" in body or name.endswith(("png", "svg")), f"{name} content")


def test_card_invalid(base_url: str) -> None:
    for name in (
        "vcard.svg",
        "vcard.png",
        "vcard.vcf",
        "mecard.svg",
        "mecard.png",
        "mecard.vcf",
    ):
        status, _, _ = request(base_url, f"/{name}?firstname=only")
        check(status == HTTPStatus.UNPROCESSABLE_ENTITY, f"invalid {name} -> {status}")


TESTS: list[Callable[[str], None]] = [
    test_home,
    test_static,
    test_form_flow,
    test_form_validation,
    test_card_outputs,
    test_card_invalid,
]


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    base_url = sys.argv[1].rstrip("/")
    wait_until_ready(base_url)
    failures = 0
    for test in TESTS:
        try:
            test(base_url)
            print(f"PASS {test.__name__}")
        except Exception as exc:  # noqa: BLE001
            failures += 1
            print(f"FAIL {test.__name__}: {exc}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
