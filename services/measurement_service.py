from datetime import datetime, timedelta

from sqlalchemy import ScalarResult
from sqlalchemy.orm import Session

from models.measurement import Measurement
from repository.measurement_repository import MeasurementRepository
from schemas.measurement import MeasurementSchema
from utils.datetime_tools import TIMEZONE


class MeasurementService:
    def __init__(self, session: Session) -> None:  # noqa: D107
        self.measurement_repo = MeasurementRepository(session)

    def get_last_measurements(self, start_time: int | None = None) -> ScalarResult[Measurement]:
        if start_time is None:
            start_time = int((datetime.now(tz=TIMEZONE) - timedelta(days=7)).timestamp())
        return self.measurement_repo.get_last_measurements(start_time=start_time)

    def save_measurement(self, body: MeasurementSchema) -> Measurement:
        new_measurement = Measurement(
            timestamp=body.timestamp,
            temperature=body.temperature,
            humidity=body.humidity,
        )
        return self.measurement_repo.save(new_measurement)
