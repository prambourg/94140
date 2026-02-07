import operator
from typing import Any, Literal

from flask import Blueprint, render_template, request
from flask_babel import gettext
from flask_pydantic import validate
from retry import retry
from sqlalchemy.exc import OperationalError

from models.base import get_session
from schemas.measurement import MeasurementSchema
from services.measurement_service import MeasurementService

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
        with get_session()() as session:
            measurement_service = MeasurementService(session)
            new_measurement = measurement_service.save_measurement(body)

        return {
            "timestamp": new_measurement.timestamp,
            "temperature": new_measurement.temperature,
            "humidity": new_measurement.humidity,
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
    with get_session()() as session:
        measurement_service = MeasurementService(session)
        datas = measurement_service.get_last_measurements()
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
