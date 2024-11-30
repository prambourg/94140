from enum import Enum

from models.base import BaseModel, db


class Campagne(Enum):
    pre2019 = -1, "pre2019"
    _2020 = 0, "2020"
    _2021 = 1, "2021"
    _2022 = 2, "2022"
    _2023 = 3, "2023"
    _2024 = 4, "2023"

    def __le__(self, other: Enum) -> bool:
        return self.value[0] <= other.value[0]

    def __lt__(self, other: Enum) -> bool:
        return self.value[0] < other.value[0]

    def __ge__(self, other: Enum) -> bool:
        return self.value[0] >= other.value[0]

    def __gt__(self, other: Enum) -> bool:
        return self.value[0] > other.value[0]

    def __str__(self) -> str:
        return self.value[1]


class Subscription(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    hello_asso_id = db.Column(db.Integer)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    campagne = db.Column(db.String(100))
    type = db.Column(db.String(100))
    amount = db.Column(db.Integer)
    email = db.Column(db.String(100))
    date = db.Column(db.DateTime)
    name = db.Column(db.String(100))
    url = db.Column(db.String(512))
    facebook = db.Column(db.String(512))
    instagram = db.Column(db.String(512))
    twitter = db.Column(db.String(512))
    member_id = db.Column(
        db.Integer, db.ForeignKey("member.id"), nullable=True,
    )

    def __repr__(self) -> str:
        return f"<Subscription Campagne {self.campagne} id {self.id}>"
