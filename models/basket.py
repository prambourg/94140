from models.base import db, BaseModel


class Basket(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String)
    date = db.Column(db.DateTime)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)
    purchase = db.relationship('Purchase', backref='basket', lazy=True)

    def __repr__(self):
        return f'<Basket l: {self.label}, d: {self.date}, s: {self.shop_id}>'

    def total_price(self):
        return sum(p.price for p in self.purchase)
