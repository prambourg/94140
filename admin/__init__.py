from flask import Flask
from flask_admin import Admin, AdminIndexView

from admin.base import AethModelView
from admin.basket import BasketAdminView
from admin.product import ProductAdminView
from admin.purchase import PurchaseAdminView
from cds.admin import init_cds_admin
from models.base import db
from models.basket import Basket
from models.measurement import Measurement
from models.product import Product
from models.purchase import Purchase
from models.shop import Shop
from utils.strings import TRESORERY_CATEGORY, WEBSITE_NAME

admin = Admin(
        name=WEBSITE_NAME,
        template_mode="bootstrap3",
        index_view=AdminIndexView(
            name=WEBSITE_NAME,
            template="index.html",
            url="/",
        ),
    )


def init_admin(app: Flask) -> None:
    admin.init_app(app)
    admin.add_view(AethModelView(Measurement, db.session, category=TRESORERY_CATEGORY))
    admin.add_view(BasketAdminView(Basket, db.session, category=TRESORERY_CATEGORY))
    admin.add_view(AethModelView(Shop, db.session, category=TRESORERY_CATEGORY))
    admin.add_view(ProductAdminView(Product, db.session, category=TRESORERY_CATEGORY))
    admin.add_view(PurchaseAdminView(Purchase, db.session, category=TRESORERY_CATEGORY))
    init_cds_admin(admin)
    admin._menu = admin._menu[1:]  # noqa: SLF001
