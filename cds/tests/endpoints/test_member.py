from collections.abc import Generator
from typing import TYPE_CHECKING, Any

import pytest
from flask.testing import FlaskClient
from sqlalchemy.orm.scoping import scoped_session

from cds.endpoints.member import DEFAULT_LIMIT

if TYPE_CHECKING:
    from jinja2 import Template


@pytest.mark.parametrize(
        ("limit", "offset", "expected", "length"),
        [
            (None, None, {"limit": DEFAULT_LIMIT, "offset": 0, "total": 5, "year": 2026}, 5),
            (0, 0, {"limit": DEFAULT_LIMIT, "offset": 0, "total": 5, "year": 2026}, 5),
            (2, None, {"limit": 2, "offset": 0, "total": 5, "year": 2026}, 2),
            (None, 3, {"limit": DEFAULT_LIMIT, "offset": 3, "total": 5, "year": 2026}, 2),
            (3, 1, {"limit": 3, "offset": 1, "total": 5, "year": 2026}, 3),
            (5, 4, {"limit": 5, "offset": 4, "total": 5, "year": 2026}, 1),
        ])
def test_get_members(
    client: FlaskClient,
    session_with_members: scoped_session,
    limit: str,
    offset: str | None,
    expected: dict[str, int | None],
    length: int,
) -> None:
    url = "/members/?"
    if limit is not None:
        url += f"limit={limit}&"
    if offset is not None:
        url += f"offset={offset}"

    response = client.get(
        url,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 200, f"Response status code: {response.status_code}"
    assert response.json["pagination"] == expected, (
        f"Expected {expected} members, but got {response.json["pagination"]}."
    )
    assert len(response.json["members"]) == length


def test_get_members_2025(client: FlaskClient, session_with_members: scoped_session) -> None:
    response = client.get("/members/?year=2025")
    assert response.status_code == 200, f"Response status code: {response.status_code}"
    expected = {"limit": DEFAULT_LIMIT, "offset": 0, "total": 1, "year": 2025}
    assert response.json["pagination"] == expected, (
        f"Expected {expected} members, but got {response.json["pagination"]}."
    )
    assert len(response.json["members"]) == 1


@pytest.mark.parametrize(
        ("param", "value", "error"),
        [
            ("limit", -2, "Limit must be non-negative"),
            ("offset", -2, "Offset must be non-negative"),
        ],
)
def test_get_members_invalid_params(client: FlaskClient, param: str, value: int, error: str) -> None:
    response = client.get(f"/members/?{param}={value}")
    assert response.status_code == 400
    assert response.json == {"error": error}


def test_home_page(client: FlaskClient, captured_templates: Generator[list, Any, None]) -> None:
    response = client.get("/liste_membres/")
    assert response.status_code == 200

    assert len(captured_templates) == 1
    template: Template
    template, _ = captured_templates[0]

    assert template.name == "index2.html"
    assert b"<title>Aeth website - VueJS</title>" in response.data
