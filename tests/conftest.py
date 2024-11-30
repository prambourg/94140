import html
from collections.abc import Generator
from datetime import datetime, timedelta
from typing import Any

import pytest
from flask import template_rendered
from flask.app import Flask
from flask.testing import FlaskClient
from flask_login import login_user, logout_user
from sqlalchemy.orm.scoping import scoped_session

from application import application
from models.base import User, db
from models.basket import Basket
from models.measurement import Measurement
from models.product import Product
from models.purchase import Purchase, PurchaseUnits
from models.shop import Shop
from utils.datetime_tools import TIMEZONE

"""
usage : pytest
usage with print : pytest -s
"""


@pytest.fixture(scope="module")
def app() -> Flask:
    application.testing = True
    return application


@pytest.fixture
def session(app: Flask) -> Generator[scoped_session, Any, None]:
    with app.app_context():
        db.session.commit()
        db.drop_all()
        db.create_all()
        yield db.session
        db.session.remove()


def create_measurements() -> None:
    now = datetime.now(tz=TIMEZONE)
    with application.app_context():
        db.session.add(
            Measurement(
                timestamp=int((now - timedelta(days=1)).timestamp()),
                temperature=20,
                humidity=50,
            ),
        )
        db.session.add(
            Measurement(
                timestamp=int((now - timedelta(days=4)).timestamp()),
                temperature=15,
                humidity=60,
            ),
        )
        db.session.add(
            Measurement(
                timestamp=int((now - timedelta(days=10)).timestamp()),
                temperature=10,
                humidity=70,
            ),
        )
        db.session.add(
            Measurement(
                timestamp=int((now - timedelta(days=30)).timestamp()),
                temperature=5,
                humidity=50,
            ),
        )
        db.session.commit()


@pytest.fixture
def create_data(session: scoped_session) -> scoped_session:
    shop = Shop(
            label="shop_label",
            city="shop_city",
            )
    session.add(shop)
    session.commit()
    product = Product(
        label="product_label",
        description="product_description",
        category="product_description",
        glucide=50,
        protide=50,
        lipide=50,
        sel=2,
        fiber=50,
        barcode=123456,
    )
    session.add(product)
    session.commit()

    basket = Basket(
        label="basket_label",
        shop_id=shop.id,
        date=datetime.now(tz=TIMEZONE),
    )
    session.add(basket)
    session.commit()

    purchase = Purchase(
        product=product,
        price=123456,
        weight=100,
        unit=PurchaseUnits.KG.value,
        basket_id=basket.id,
    )
    session.add(purchase)
    session.commit()
    return session


@pytest.fixture
def captured_templates(app: Flask) -> Generator[list, Any, None]:
    recorded = []

    def record(sender, template, context, **extra) -> None:  # noqa: ANN001, ANN003
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


@pytest.fixture
def login_as_admin(
        client: FlaskClient,
        session: scoped_session,
    ) -> None:  # type: ignore  # noqa: PGH003
    user = User(username="admin", password="foobar")  # noqa: S106
    session.add(user)
    session.commit()
    login_user(user)
    yield
    logout_user()


@pytest.fixture
def login_as_user(
        client: FlaskClient,
        session: scoped_session,
    ) -> None:  # type: ignore  # noqa: PGH003
    user = User(username="username", password="username")  # noqa: S106
    session.add(user)
    session.commit()
    login_user(user)
    yield
    logout_user()


def htmlify(s: str) -> bytes:
    return html.escape(s).replace("&#x27;", "&#39;").encode()
