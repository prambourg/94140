from collections.abc import Generator
from typing import TYPE_CHECKING, Any

from flask.testing import FlaskClient

if TYPE_CHECKING:
    from jinja2 import Template


def test_index(client: FlaskClient, captured_templates: Generator[list, Any, None]) -> None:
    response = client.get("/")

    assert response.status_code == 200

    assert len(captured_templates) == 1
    template: Template
    template, _ = captured_templates[0]

    assert template.name == "index.html"
    assert b"<title>Home - new AWS</title>" in response.data


def test_camera(client: FlaskClient, captured_templates: Generator[list, Any, None]) -> None:
    response = client.get("/camera/")

    assert response.status_code == 200

    assert len(captured_templates) == 1
    template: Template
    template, _ = captured_templates[0]

    assert template.name == "camera.html"
    assert b"<title>Camera</title>" in response.data


def test_cv(client: FlaskClient) -> None:
    response = client.get("/CV/")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/pdf"
    assert response.data.startswith(b"%PDF")


def test_ads(client: FlaskClient) -> None:
    response = client.get("/ads.txt")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/plain; charset=utf-8"
