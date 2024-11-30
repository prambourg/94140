from __future__ import annotations

from sqlalchemy.orm import Mapped, validates

from models.base import BaseModel, intpk


class Measurement(BaseModel):
    id: Mapped[intpk]
    timestamp: Mapped[int]
    temperature: Mapped[float | None]
    humidity: Mapped[float | None]

    @validates("temperature")
    def temperature_validation(self, key: str, value: str) -> float | None:  # noqa: ARG002, PLR6301
        if value is None:
            return value
        if value == "None" or float(value) < 0.0:
            return None
        return value

    @validates("humidity")
    def humidity_validation(self, key: str, value: str) -> float | None:  # noqa: ARG002, PLR6301
        if value is None:
            return value
        if value == "None" or float(value) >= 100.0:  # noqa: PLR2004
            return None
        return value

    def __repr__(self) -> str:
        return f"<Measurement {self.temperature} {self.humidity} {self.timestamp}>"

    def __str__(self) -> str:
        return f"<Measurement {self.temperature} {self.humidity} {self.timestamp}>"
