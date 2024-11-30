from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from models.measurement import Measurement

if TYPE_CHECKING:
    from flask.testing import FlaskClient
    from sqlalchemy.orm.scoping import scoped_session


@pytest.mark.parametrize(
    "data",
    [
        (123456, 25.0, 40.4),
        (123456, None, 40.4),
        (123456, 25.0, None),
    ],
)
def test_measurement(session: scoped_session, data: tuple[float | None]) -> None:
    timestamp, temperature, humidity = data
    # before insertion
    assert len(session.execute(select(Measurement)).scalars().all()) == 0

    # insertion
    measurement = Measurement(
        timestamp=timestamp, temperature=temperature, humidity=humidity,
    )
    session.add(measurement)
    session.commit()

    db_measurement: Measurement = session.execute(select(Measurement)).scalar_one()

    assert db_measurement.timestamp == timestamp == measurement.timestamp
    assert db_measurement.temperature == temperature == measurement.temperature
    assert db_measurement.humidity == humidity == measurement.humidity


def test_measurement_null_timestamp(session: scoped_session) -> None:
    # before insertion
    assert len(session.execute(select(Measurement)).scalars().all()) == 0

    # insertion
    measurement = Measurement(timestamp=None, temperature=25.0, humidity=30.0)
    session.add(measurement)
    with pytest.raises(
        IntegrityError,
        match="NOT NULL constraint failed: measurement.timestamp",
    ):
        session.commit()


def test_abnormal_temperature(client: FlaskClient, session: scoped_session) -> None:
    m = Measurement(timestamp=123456, temperature=-15.0, humidity=50.0)
    session.add(m)
    session.commit()

    db_m = session.execute(select(Measurement)).scalar_one()

    assert db_m.temperature is None


def test_abnormal_humidity(client: FlaskClient, session: scoped_session) -> None:
    m = Measurement(timestamp=123456, temperature=20.0, humidity=123456)
    session.add(m)
    session.commit()

    db_m = session.execute(select(Measurement)).scalar_one()

    assert db_m.humidity is None
