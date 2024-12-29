from collections.abc import Generator
from typing import TYPE_CHECKING, Any

from flask.testing import FlaskClient

if TYPE_CHECKING:
    from jinja2 import Template


def test_python_home(client: FlaskClient, captured_templates: Generator[list, Any, None]) -> None:
    response = client.get("/python/")

    assert response.status_code == 200

    assert len(captured_templates) == 1
    template: Template
    template, _ = captured_templates[0]

    assert template.name == "python/base.html"
    assert b"<title>Python tutorial</title>" in response.data


def test_python_about(client: FlaskClient, captured_templates: Generator[list, Any, None]) -> None:
    response = client.get("/python/about/")

    assert response.status_code == 200

    assert len(captured_templates) == 1
    template: Template
    template, _ = captured_templates[0]

    assert template.name == "python/about.html"
    assert b"<title>Python tutorial - About</title>" in response.data


def test_python_csv(client: FlaskClient, captured_templates: Generator[list, Any, None]) -> None:
    response = client.get("/python/csv/")

    assert response.status_code == 200

    assert len(captured_templates) == 1
    template: Template
    template, _ = captured_templates[0]

    assert template.name == "python/csv.html"
    assert b"<title>Python tutorial - CSV</title>" in response.data


def test_python_retry(client: FlaskClient, captured_templates: Generator[list, Any, None]) -> None:
    response = client.get("/python/retry/")

    assert response.status_code == 200

    assert len(captured_templates) == 1
    template: Template
    template, _ = captured_templates[0]

    assert template.name == "python/retry.html"
    assert b"<title>Python tutorial - Retry</title>" in response.data
