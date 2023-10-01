from enum import Enum

from models.base import BaseModel, db


class PurchaseUnits(Enum):
    KG = 'Kg'
    CL = 'Cl'
    L = 'L'
    u = 'u'
    NULL = None


class Purchase(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=True)
    unit = db.Column(db.Integer, nullable=True)
    basket_id = db.Column(db.Integer, db.ForeignKey('basket.id'), nullable=False)

    @property
    def normalized_price(self):
        if self.unit == PurchaseUnits.KG.value:
            price = int(self.price / self.weight) / 100
            print(f'{self.price} € - {self.weight} kg - {price} €/kg')
            return price
        if self.unit == PurchaseUnits.u.value:
            price = int(self.price / self.weight) / 100
            return price
        return self.price

    def __repr__(self):
        return f'<{self.product.description}, b: {self.basket.label}, price: {self.price}>'

