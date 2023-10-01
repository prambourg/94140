from flask import url_for
from flask_admin.form import Select2Field
from markupsafe import Markup

from admin import AethModelView
from models.shop import Shop


def get_shops_choices():
    shops = Shop.query.all()
    choices = [(shops.id, shops.label) for shops in shops]
    return choices


class BasketAdminView(AethModelView):
    column_list = ('label', 'date', 'purchase', 'shop', 'total_price')
    column_details_list = ('label', 'date', 'purchase', 'shop', 'total_price')
    form_columns = ('label', 'date', 'shop_id')

    form_overrides = {
        'shop_id': Select2Field,
    }

    form_args = {
        'shop_id': {
            'coerce': int,
            'choices': get_shops_choices,
        },
    }

    def format_shop(self, context, model, name):
        return Markup('<a href="{url}" title="Link to Shop">{shop}</a>'.format(
            url=url_for('shop.details_view', id=model.shop.id),
            shop=model.shop.label)
        )

    def format_purchase(self, context, model, name):
        return Markup('<br>'.join('<a href="{url}" title="Link to Purchase">{purchase}</a>'.format(
            url=url_for('purchase.details_view', id=p.id),
            purchase=p.product.label)
            for p in model.purchase))

    column_formatters = {
        'shop': format_shop,
        'purchase': format_purchase,
    }
