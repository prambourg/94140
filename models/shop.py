from models.base import BaseModel, db


class Shop(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String)
    city = db.Column(db.String)
    basket = db.relationship('Basket', backref='shop', lazy=True)

    def __repr__(self):
        return f'<Shop l: {self.label}, c: {self.city}>'
