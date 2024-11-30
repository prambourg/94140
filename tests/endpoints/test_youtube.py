from collections.abc import Generator
from typing import TYPE_CHECKING, Any

import pytest
from flask.testing import FlaskClient

from endpoints.youtube import YOUTUBE_URLS

if TYPE_CHECKING:
    from jinja2 import Template


@pytest.mark.parametrize(("uid", "title"), YOUTUBE_URLS.items())
def test_youtube_urls(
    client: FlaskClient,
    captured_templates: Generator[list, Any, None],
    uid: str,
    title: str,
) -> None:
    response = client.get(
        f"/youtube/{uid}/",
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 200

    assert len(captured_templates) == 1
    template: Template
    context: dict[str, Any]
    template, context = captured_templates[0]

    assert template.name == "youtube.html"
    assert context["uid"] == uid
    assert context["title"] == title
