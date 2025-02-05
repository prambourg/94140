from sqlalchemy import ScalarResult, select

from models.measurement import Measurement
from repository.base_repository import BaseRepository


class MeasurementRepository(BaseRepository):
    def get_last_measurements(self, start_time: int) -> ScalarResult[Measurement]:
        stmt = select(Measurement).where(Measurement.timestamp >= start_time)
        return self.session.execute(stmt).scalars()
