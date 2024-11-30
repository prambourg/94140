import csv
import os

from models.base import db
from models.measurement import Measurement


def dict_filter(it, *keys):
    for d in it:
        yield dict((k, d[k]) for k in keys)


def import_measurements() -> None:
    csv_path = os.path.join("static", "data.csv")
    fieldnames = ["timestamp", "temperature", "humidity"]
    batch_size = 500
    with open(csv_path, "r", newline="") as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(dict_filter(reader, *fieldnames)):
            print(i, row)
            m = Measurement(
                timestamp=row["timestamp"],
                temperature=row["temperature"],
                humidity=row["humidity"],
            )
            db.session.add(m)
            if (i + 1) % batch_size == 0:
                db.session.commit()


def export_measurements(delete=False) -> None:
    csv_path = os.path.join("static", "data.csv")
    fieldnames = ["id", "timestamp", "temperature", "humidity"]
    with open(csv_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        measurements = Measurement.query.all()
        for measurement in measurements:
            writer.writerow(measurement.row2dict())
    if delete:
        db.session.query(Measurement).delete()
        db.session.commit()
