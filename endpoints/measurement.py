from flask import Blueprint, request, render_template
from flask_babel import gettext
from flask_pydantic import validate
from retry import retry
from sqlalchemy.exc import OperationalError

from models.measurement import Measurement, db
from schemas.measurement import MeasurementSchema

measurement_blueprint = Blueprint('measurement_blueprint', __name__)


@measurement_blueprint.route('/measurement', methods=["POST", ])
@validate()
@retry(OperationalError, tries=10, delay=1)
def measurement_create(body: MeasurementSchema):
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


@measurement_blueprint.route("/measurements", methods=["GET", ])
@retry(OperationalError, tries=10, delay=1)
def measurements():
    datas = Measurement.query.all()
    t = []
    h = []
    for data in datas:
        t.append(
            {"x": int(str(data.timestamp).split(".")[0] + "000"), "y": data.temperature}
        )
        h.append(
            {"x": int(str(data.timestamp).split(".")[0] + "000"), "y": data.humidity}
        )
    t.sort(key=lambda temp: temp["x"])
    h.sort(key=lambda hum: hum["x"])
    return render_template("measurements.html", temperatures=t, humidities=h, title=gettext('Measurement'))
