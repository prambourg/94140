from flask import url_for
from flask_admin.contrib.sqla.filters import EnumFilterInList
from markupsafe import Markup
from sqlalchemy import select

from admin.base import CdsModelView
from models.base import db
from models.cds.subscription import Subscription

CAMPAGNES = (
    (("valider-l-adhesion-au-cafe-des-sciences",), "pré_2020"),
    (
        (
            "adhesion-2020-au-cafe-des-sciences",
            "adhesion-2020-au-cafe-des-sciences-2",
        ),
        "2020",
    ),
    (
        (
            "cotisation-aux-cafe-des-sciences-annee-2021",
            "rattrapage-adhesion-2021-au-cafe-des-sciences-2",
        ),
        "2021",
    ),
    (
        ("cotisation-2022-au-cafe-des-sciences", "rattrapage-adhesion-2022"),
        "2022",
    ),
    ("cotisation-2023-au-cafe-des-sciences", "2023"),
    ("cotisation-2023-au-cafe-des-sciences", "2024"),
    ("2", "don"),
)

CAMPAGNES_YEAR = {
    "valider-l-adhesion-au-cafe-des-sciences": "pré-2019",
    "2": "don",
    "adhesion-2020-au-cafe-des-sciences": "2020",
    "adhesion-2020-au-cafe-des-sciences-2": "2020",
    "cotisation-aux-cafe-des-sciences-annee-2021": "2021",
    "rattrapage-adhesion-2021-au-cafe-des-sciences-2": "2021",
    "cotisation-2022-au-cafe-des-sciences": "2022",
    "rattrapage-adhesion-2022": "2022",
    "cotisation-2023-au-cafe-des-sciences": "2023",
    "cotisation-2024-au-cafe-des-sciences": "2024",
}


def get_campaigns() -> tuple[tuple[str]]:
    unique_campaign: list[Subscription] = db.session.execute(select(Subscription.campagne).distinct()).scalars().all()
    return ((s, s) for s in unique_campaign)


class HelloAssoView(CdsModelView):
    column_filters = [
        EnumFilterInList(
            column=Subscription.campagne,
            name="Campagne",
            options=get_campaigns,
        ),
        "name",
        "first_name",
        "last_name",
        "email",
    ]
    can_create = True
    can_edit = True
    can_delete = True
    column_exclude_list = [
        "hello_asso_id",
    ]
    can_export = False
    column_default_sort = ("hello_asso_id", True)

    column_list = (
        "first_name",
        "last_name",
        "campagne",
        "type",
        "amount",
        "email",
        "date",
        "name",
        "url",
        "facebook",
        "instagram",
        "twitter",
        "member",
    )

    column_details_list = (
        "first_name",
        "last_name",
        "campagne",
        "type",
        "amount",
        "email",
        "date",
        "name",
        "url",
        "facebook",
        "instagram",
        "twitter",
        "member",
    )

    def format_member(self, context, model, name):
        if model.member is not None:
            return Markup(
                '<a href="{url}" title="Link to Member">{member}</a>'.format(
                    url=url_for('member.details_view', id=model.member_id),
                    member=model.member.name,
                ),
            )
        return Markup()

    column_formatters = {
        "member": format_member,
    }
