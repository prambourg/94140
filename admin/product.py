from flask import request, url_for
from flask_admin import expose
from flask_admin.form import Select2Field
from markupsafe import Markup
from sqlalchemy import select

from admin import AethModelView
from models.base import db
from models.product import ProductCategory
from models.purchase import Purchase


class ProductAdminView(AethModelView):
    details_template = "admin/product_details.html"

    column_list = (
        "label",
        "description",
        "category",
        "glucide",
        "protide",
        "lipide",
        "sel",
        "fiber",
        "purchase",
        "barcode",
        "average_price",
        "n_total",
    )

    column_sortable_list = [
        "n_total",
    ]

    column_details_list = (
        "label",
        "description",
        "category",
        "glucide",
        "protide",
        "lipide",
        "sel",
        "fiber",
        "purchase",
        "barcode",
        "average_price",
    )

    @expose("/details/", methods=("GET", "POST"))
    def details_view(self):
        data = [
            {
                "x": int(str(int(purchase.basket.date.timestamp())) + "000"),
                "y": purchase.normalized_price,
            }
            for purchase in db.session.execute(
                select(Purchase).where(Purchase.product_id == request.args.get("id", "")),
            ).scalars()
        ]
        self._template_args["data"] = data
        print(data)
        return super(ProductAdminView, self).details_view()

    def format_purchase(self, context, model, name):
        return Markup(
            "<br>".join(
                '<a href="{url}" title="Link to Purchase">{purchase}</a>'.format(
                    url=url_for("purchase.details_view", id=p.id),
                    purchase=p.basket.label,
                )
                for p in model.purchase
            ),
        )

    column_formatters = {
        "purchase": format_purchase,
    }
    form_overrides = {
        "category": Select2Field,
    }

    form_args = {
        "category": {
            "coerce": str,
            "choices": [(item.value, item.value) for item in ProductCategory],
        }
    }
