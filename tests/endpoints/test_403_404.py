from collections.abc import Generator
from typing import TYPE_CHECKING, Any

from flask.testing import FlaskClient

if TYPE_CHECKING:
    from jinja2 import Template


def test_404(client: FlaskClient, captured_templates: Generator[list, Any, None]) -> None:
    response = client.get("/foobar/")

    assert response.status_code == 200

    assert len(captured_templates) == 1
    template: Template
    template, _ = captured_templates[0]

    assert template.name == "404.html"
    assert b"<title>Not found</title>" in response.data


def test_403(client: FlaskClient, captured_templates: Generator[list, Any, None]) -> None:
    response = client.get("/membresRelance2021/")

    assert response.status_code == 200

    assert len(captured_templates) == 1
    template: Template
    template, _ = captured_templates[0]

    assert template.name == "403.html"
    assert b"<title>Acc\xc3\xa8s refus\xc3\xa9</title>" in response.data
