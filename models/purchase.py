from models.base import BaseModel, db


class Purchase(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    basket_id = db.Column(db.Integer, db.ForeignKey('basket.id'), nullable=False)

    def __repr__(self):
        return f'<Purchase p: {self.product_id}, b: {self.basket_id}, price: {self.price}, date: {self.date}>'
