import operator
from datetime import datetime, timedelta
from typing import Any, Literal

from flask import Blueprint, render_template, request
from flask_babel import gettext
from flask_pydantic import validate
from retry import retry
from sqlalchemy import select
from sqlalchemy.exc import OperationalError

from models.base import db
from models.measurement import Measurement
from schemas.measurement import MeasurementSchema
from utils.datetime_tools import TIMEZONE

measurement_blueprint = Blueprint("measurement_blueprint", __name__)


@measurement_blueprint.route(
    "/measurement",
    methods=[
        "POST",
    ],
)
@validate()
@retry(OperationalError, tries=10, delay=1)
def measurement_create(body: MeasurementSchema) -> (tuple[dict[str, Any], Literal[201]] | None):
    if request.method == "POST":
        measurement = Measurement(
            timestamp=body.timestamp,
            temperature=body.temperature,
            humidity=body.humidity,
        )
        try:
            db.session.add(measurement)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        return {
            "timestamp": measurement.timestamp,
            "temperature": measurement.temperature,
            "humidity": measurement.humidity,
        }, 201
    return None


@measurement_blueprint.route(
    "/measurements/",
    methods=[
        "GET",
    ],
)
@retry(OperationalError, tries=10, delay=1)
def measurements() -> str:
    # date_debut, date_fin, granularité/step (default=10min, sinon heure, demi journée, journée, semaine, mois, an)
    epoch_last_week = int((datetime.now(tz=TIMEZONE) - timedelta(days=7)).timestamp())
    datas = db.session.execute(select(Measurement).where(Measurement.timestamp >= epoch_last_week)).scalars()
    t = []
    h = []
    for data in datas:
        temp = "null" if data.temperature is None else data.temperature

        hum = "null" if data.humidity is None else data.humidity
        t.append(
            {"x": int(str(data.timestamp).split(".")[0] + "000"), "y": temp},
        )
        h.append(
            {"x": int(str(data.timestamp).split(".")[0] + "000"), "y": hum},
        )
    t.sort(key=operator.itemgetter("x"))
    h.sort(key=operator.itemgetter("x"))

    if not t:
        t = [{"y": None}]
    if not h:
        h = [{"y": None}]
    return render_template(
        "measurements.html",
        temperatures=t,
        humidities=h,
        title=gettext("Measurement"),
    )
