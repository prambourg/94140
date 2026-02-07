from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from flask import url_for
from flask_admin.form import Select2Field
from markupsafe import Markup
from sqlalchemy import select

from admin.base import AethModelView
from models.base import get_session
from models.shop import Shop

if TYPE_CHECKING:
    from collections.abc import Callable

    from sqlalchemy.orm import Session

    from models.basket import Basket


def get_shops_choices() -> list[tuple]:
    session: Session
    with get_session()() as session:
        shops = session.execute(select(Shop)).scalars()
        return [(shops.id, shops.label) for shops in shops]


class BasketAdminView(AethModelView):
    column_list = ("label", "date", "purchase", "shop", "total_price")
    column_details_list = ("label", "date", "purchase", "shop", "total_price")
    form_columns = ("label", "date", "shop_id")

    form_overrides: ClassVar[dict[str, Callable]] = {
        "shop_id": Select2Field,
    }

    form_args: ClassVar[dict[str, Callable]] = {
        "shop_id": {
            "coerce": int,
            "choices": get_shops_choices,
        },
    }

    def format_shop(self, context, model: Basket, name) -> Markup:
        return Markup(
            '<a href="{url}" title="Link to Shop">{shop}</a>'.format(
                url=url_for("shop.details_view", id=model.shop.id),
                shop=model.shop.label,
            ),
        )

    def format_purchase(self, context, model: Basket, name) -> Markup:
        return Markup(
            "<br>".join(
                '<a href="{url}" title="Link to Purchase">{purchase}</a>'.format(
                    url=url_for("purchase.details_view", id=p.id),
                    purchase=p.product.label,
                )
                for p in model.purchase
            ),
        )

    column_formatters: ClassVar[dict[str, Callable]] = {
        "shop": format_shop,
        "purchase": format_purchase,
    }
