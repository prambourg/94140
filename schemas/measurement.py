from __future__ import annotations

from pydantic import BaseModel


class MeasurementSchema(BaseModel):
    timestamp: int
    temperature: float | None
    humidity: float | None
