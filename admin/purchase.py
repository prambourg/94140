from flask import url_for
from flask_admin import expose
from flask_admin.contrib.sqla.filters import BaseSQLAFilter
from flask_admin.form import Select2Field
from markupsafe import Markup
from sqlalchemy import select

from admin.base import AethModelView
from models.base import db, intpk
from models.basket import Basket
from models.product import Product
from models.purchase import Purchase, PurchaseUnits


class FilterByProduct(BaseSQLAFilter):
    def apply(self, query, value, alias=None):
        return query.join(Purchase.products).filter(Product.id == value)

    def operation(self) -> str:
        return "equals"

    def get_options(self, view) -> list[tuple[intpk, str]]:
        stmt = select(Product.id, Product.barcode, Product.label)
        products: list[Product] = db.session.execute(stmt).all()
        return [(product.id, f"{product.barcode} - {product.label}") for product in products]


def get_products_choices():
    products = Product.query.all()
    choices = (
        (product.id, f"{product.barcode} - {product.label}")
        for product in products
    )
    return choices


def get_baskets_choices():
    baskets = Basket.query.all()
    choices = [(basket.id, basket.label) for basket in baskets]
    return choices


class PurchaseAdminView(AethModelView):
    column_list = ("price", "product", "basket", "weight", "unit")
    column_details_list = ("price", "product", "basket", "weight", "unit")
    form_columns = ("price", "product_id", "basket_id", "weight", "unit")

    column_editable_list = (
        "price",
        "weight",
    )

    form_overrides = {
        "product_id": Select2Field,
        "basket_id": Select2Field,
        "unit": Select2Field,
    }

    form_args = {
        "product_id": {
            "coerce": int,
            "choices": get_products_choices,
        },
        "basket_id": {
            "coerce": int,
            "choices": get_baskets_choices,
        },
        "unit": {
            "coerce": str,
            "choices": [(item.value, item.value) for item in PurchaseUnits],
        },
    }

    column_filters = [
        FilterByProduct(column=None, name="Produits"),
    ]

    def format_product(self, context, model, name) -> Markup:
        return Markup(
            '<a href="{url}" title="Link to Product">{product}</a>'.format(
                url=url_for("product.details_view", id=model.product.id),
                product=model.product.label,
            ),
        )

    def format_basket(self, context, model, name) -> Markup:
        return Markup(
            '<a href="{url}" title="Link to Basket">{basket}</a>'.format(
                url=url_for("basket.details_view", id=model.basket.id),
                basket=model.basket.label,
            ),
        )

    def format_price(self, context, model, name) -> float:
        return float(model.price / 100)

    column_formatters = {
        "product": format_product,
        "basket": format_basket,
        "price": format_price,
    }

    @expose("/")
    def index_view(self):
        self._refresh_filters_cache()
        return super(PurchaseAdminView, self).index_view()
