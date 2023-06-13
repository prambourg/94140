from datetime import date

from models.basket import Basket
from models.measurement import db
from models.product import Product
from models.purchase import Purchase
from models.shop import Shop

models_app = (Basket, Product, Purchase, Shop)


def delete_all():
    for model in models_app:
        db.session.query(model).delete()
    db.session.commit()


def add_shops():
    s = Shop(label='Carrefour City', city='Montreuil')
    db.session.add(s)
    db.session.commit()


def add_products():
    p = Product(description='Poulet',
                category='Aliment',
                glucide='10',
                protide='25',
                lipide='2',
                sel='1',
                fiber='0')
    db.session.add(p)
    p = Product(description='Poisson',
                category='Aliment',
                glucide='0',
                protide='50',
                lipide='0',
                sel='10',
                fiber='5')
    db.session.add(p)
    db.session.commit()


def add_baskets():
    shop_id = Shop.query.filter().first().id
    b = Basket(label='test panier',
               date=date.today(),
               shop_id=shop_id)
    db.session.add(b)
    db.session.commit()


def add_purchases():
    products = Product.query.filter().all()
    basket_id = Basket.query.filter().first().id
    for product in products:
        p = Purchase(product_id=product.id,
                     price=50,
                     date=date.today(),
                     basket_id=basket_id)
        db.session.add(p)

    for product in products:
        p = Purchase(product_id=product.id,
                     price=500,
                     date=date.today(),
                     basket_id=basket_id)
        db.session.add(p)

    db.session.commit()


def add_props():
    add_shops()
    add_products()
    add_baskets()
    add_purchases()
    