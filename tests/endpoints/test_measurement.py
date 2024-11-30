from __future__ import annotations

import json
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any

import pytest

from models.measurement import Measurement
from utils.datetime_tools import TIMEZONE

if TYPE_CHECKING:
    from collections.abc import Generator

    from flask.testing import FlaskClient
    from jinja2 import Template
    from sqlalchemy.orm.scoping import scoped_session


@pytest.mark.parametrize(
    "data",
    [
        (123456, 25.0, 40.4),
        (123456, None, 40.4),
        (123456, 25.0, None),
    ],
)
def test_post(client: FlaskClient, session: scoped_session, data: tuple[float | None]) -> None:
    timestamp, temperature, humidity = data
    response = client.post(
        "/measurement",
        data=json.dumps(
            {
                "timestamp": timestamp,
                "temperature": temperature,
                "humidity": humidity,
            },
        ),
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 201

    measurement: Measurement = Measurement.query.one()

    assert measurement.timestamp == timestamp
    assert measurement.temperature == temperature
    assert measurement.humidity == humidity


def test_post_null_timestamp(client: FlaskClient, session: scoped_session) -> None:
    response = client.post(
        "/measurement",
        data=json.dumps(
            {
                "timestamp": None,
                "temperature": 25.0,
                "humidity": 40.4,
            },
        ),
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 400


def test_get_measurements(
    client: FlaskClient,
    session: scoped_session,
    captured_templates: Generator[list, Any, None],
) -> None:
    now = datetime.now(tz=TIMEZONE)
    measurement_0 = Measurement(
        timestamp=int(now.timestamp()), temperature=50.0, humidity=15.0,
    )
    measurement_1 = Measurement(
        timestamp=int((now - timedelta(days=3)).timestamp()), temperature=40.0, humidity=25.0,
    )
    measurement_2 = Measurement(
        timestamp=int((now - timedelta(days=30)).timestamp()), temperature=30.0, humidity=35.0,
    )
    session.add(measurement_0)
    session.add(measurement_1)
    session.add(measurement_2)
    session.commit()

    response = client.get(
        "/measurements/",
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 200

    assert len(captured_templates) == 1
    template: Template
    context: dict[str, Any]
    template, context = captured_templates[0]

    assert template.name == "measurements.html"
    assert "temperatures" in context
    assert context["temperatures"] == [
        {"x": int(str(measurement_1.timestamp) + "000"), "y": measurement_1.temperature},
        {"x": int(str(measurement_0.timestamp) + "000"), "y": measurement_0.temperature},
    ]
    assert "humidities" in context
    assert context["humidities"] == [
        {"x": int(str(measurement_1.timestamp) + "000"), "y": measurement_1.humidity},
        {"x": int(str(measurement_0.timestamp) + "000"), "y": measurement_0.humidity},
    ]
