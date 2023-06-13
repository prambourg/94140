from pydantic import BaseModel


class MeasurementSchema(BaseModel):
    timestamp: int
    temperature: float
    humidity: float
