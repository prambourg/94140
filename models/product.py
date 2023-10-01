from enum import Enum

from sqlalchemy import select, func
from sqlalchemy.ext.hybrid import hybrid_property

from models.base import BaseModel, db
from models.purchase import Purchase


class ProductCategory(Enum):
    ALIMENT = 'Aliment'
    HYGIENE = 'Hygiène'
    ALCOHOL = 'Alcool'
    OTHER = 'Autre'


class Product(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(100), nullable=True)
    glucide = db.Column(db.Integer, nullable=True)
    protide = db.Column(db.Integer, nullable=True)
    lipide = db.Column(db.Integer, nullable=True)
    sel = db.Column(db.Integer, nullable=True)
    fiber = db.Column(db.Integer, nullable=True)
    purchase = db.relationship('Purchase', backref='product', lazy=True)
    barcode = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'<Product d: {self.description}>'

    @property
    def average_price(self) -> float:
        purchases = Purchase.query.filter(Purchase.product_id == self.id).all()
        return (int(sum(p.normalized_price * 100 for p in purchases) / len(purchases))) / 100

    @hybrid_property
    def n_total(self) -> int:
        return len(self.purchase)

    @n_total.expression
    def n_total(cls):
        return select(func.count(Purchase.id)).where(Purchase.product_id == cls.id).label('n_total')
