from flask import Flask
from flask_admin import Admin, AdminIndexView

from admin.base import AethModelView
from admin.basket import BasketAdminView
from admin.member import (
    Member2023ListView,
    Member2024ListView,
    MemberToContact2020,
    MemberToContact2021,
    MemberToContact2022,
    MemberToContact2023,
    MemberView,
)
from admin.product import ProductAdminView
from admin.purchase import PurchaseAdminView
from admin.subscription import HelloAssoView
from models.base import db
from models.basket import Basket
from models.cds.member import Member
from models.cds.subscription import Subscription
from models.measurement import Measurement
from models.product import Product
from models.purchase import Purchase
from models.shop import Shop
from utils.strings import CDS_CATEGORY, TRESORERY_CATEGORY, WEBSITE_NAME

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
    admin.add_view(
        HelloAssoView(
            Subscription,
            db.session,
            name="Historique adhésions",
            category=CDS_CATEGORY,
        ),
    )
    admin.add_view(
        Member2023ListView(
            Member,
            db.session,
            name="Liste des membres publique 2023",
            endpoint="liste_membres_2023",
            category=CDS_CATEGORY,
        ),
    )
    admin.add_view(
        Member2024ListView(
            Member,
            db.session,
            name="Liste des membres publique 2024",
            endpoint="liste_membre",
            category=CDS_CATEGORY,
        ),
    )
    admin.add_view(
        MemberView(
            Member,
            db.session,
            name="Liste des membres détaillée",
            category=CDS_CATEGORY,
        ),
    )
    admin.add_view(
        MemberToContact2023(
            Member,
            db.session,
            name="A relancer 2023",
            endpoint="membresRelance2023",
            category=CDS_CATEGORY,
        ),
    )
    admin.add_view(
        MemberToContact2022(
            Member,
            db.session,
            name="A relancer 2022",
            endpoint="membresRelance2022",
            category=CDS_CATEGORY,
        ),
    )
    admin.add_view(
        MemberToContact2021(
            Member,
            db.session,
            name="A relancer 2021",
            endpoint="membresRelance2021",
            category=CDS_CATEGORY,
        ),
    )
    admin.add_view(
        MemberToContact2020(
            Member,
            db.session,
            name="A relancer 2020",
            endpoint="membresRelance2020",
            category=CDS_CATEGORY,
        ),
    )
    admin._menu = admin._menu[1:]  # noqa: SLF001
