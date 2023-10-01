from models.base import db, BaseModel


class Order(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    hello_asso_id = db.Column(db.Integer)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    campagne = db.Column(db.String(100))
    type = db.Column(db.String(100))
    amount = db.Column(db.Integer)
    email = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    name = db.Column(db.String(100))
    url = db.Column(db.String(100))
    facebook = db.Column(db.String(100))
    instagram = db.Column(db.String(100))
    twitter = db.Column(db.String(100))
