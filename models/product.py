from models.base import BaseModel, db
from models.purchase import Purchase


class Product(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    category = db.Column(db.String)
    glucide = db.Column(db.Integer)
    protide = db.Column(db.Integer)
    lipide = db.Column(db.Integer)
    sel = db.Column(db.Integer)
    fiber = db.Column(db.Integer)
    purchase = db.relationship('Purchase', backref='product', lazy=True)

    def __repr__(self):
        return f'<Product d: {self.description}>'

    def average_price(self):
        purchases = Purchase.query.filter(Purchase.product_id == self.id).all()
        return sum(p.price for p in purchases) / len(purchases)
