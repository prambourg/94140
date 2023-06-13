from models.base import BaseModel, db


class Measurement(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Integer, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Measurement {self.temperature} {self.humidity} {self.timestamp}>"

    def __str__(self):
        return f"<Measurement {self.temperature} {self.humidity} {self.timestamp}>"
