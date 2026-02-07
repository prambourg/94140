import re
from collections.abc import Callable
from typing import ClassVar

from flask import flash, url_for
from flask_admin.actions import action
from flask_sqlalchemy.query import Query
from markupsafe import Markup
from sqlalchemy import func, select

from admin.base import CdsModelView
from cds.models.member import Member
from cds.models.subscription import Subscription
from models.base import db


class MemberView(CdsModelView):
    can_view_details = True
    column_list = (
        "name",
        "email",
        "subscriptions",
        "up_to_date",
        "confirmed_departure",
        "mail_sent",
    )

    column_filters = (
        "name",
        "email",
        "subscriptions",
        "confirmed_departure",
        "mail_sent",
    )

    column_default_sort = "name"

    column_details_list = (
        "name",
        "email",
        "first_name",
        "last_name",
        "subscriptions",
        "up_to_date",
        "is_2026",
        "is_2025",
        "is_2024",
        "is_2023",
        "is_2022",
        "is_2021",
        "is_2020",
        "confirmed_departure",
        "mail_sent",
    )

    def format_subscriptions(self, context, model, name) -> Markup:
        return Markup(
            "<br>".join(
                '<a href="{url}" title="Link to Subscription">{subscription}</a>'.format(
                    url=url_for("subscription.details_view", id=s.id),
                    subscription=s.campagne,
                )
                for s in model.subscriptions
            ),
        )

    column_formatters: ClassVar[dict[str, Callable]] = {
        "subscriptions": format_subscriptions,
    }

    column_formatters_detail: ClassVar[dict[str, Callable]] = {
        "subscriptions": format_subscriptions,
    }

    @action(
        "Fusion",
        "Fusion members",
        "Êtes vous sûr de vouloir fusionner la sélection de membres ?",
    )
    def action_fusion(self, ids) -> None:
        subscriptions: list[Subscription] = (
            db.session.execute(
            select(Subscription)
            .join(Member, Subscription.member_id == Member.id)
            .filter(Member.id.in_(ids))
            .order_by(Subscription.id.desc()),
            )
            .scalars()
            .all()
        )

        master_member_id = subscriptions[0].member_id
        master_member = subscriptions[0].member
        for sub in subscriptions[1:]:
            if sub.member.id != master_member_id:
                db.session.delete(sub.member)
                sub.member_id = master_member_id
                sub.member = master_member
        db.session.commit()
        flash(f"{ids} ont fusionné")

    @action(
        "Split",
        "Split member",
        "Êtes vous sûr de vouloir spliter la sélection de membres ?",
    )
    def action_split(self, ids) -> None:
        subscriptions = (
            db.session.execute(
                select(Subscription)
                .join(Member, Subscription.member_id == Member.id)
                .filter(Member.id.in_(ids))
                .order_by(Subscription.id.desc()),
            )
            .scalars()
            .all()
        )
        s: Subscription
        for s in subscriptions:
            db.session.delete(s.member)
            new_member = Member(
                name=s.name,
                email=s.email,
                first_name=s.first_name,
                last_name=s.last_name,
                confirmed_departure=False,
                mail_sent=False,
            )
            s.member = new_member
            s.member_id = new_member.id
            db.session.add(new_member)
        db.session.commit()
        flash(f"{ids} ont splité")


class Member2023ListView(CdsModelView):
    can_create = False
    can_edit = False
    can_delete = False
    can_view_details = False

    column_default_sort = "name"

    column_list = ("name", "url")

    column_labels: ClassVar[dict[str, str]] = {"name": "Pseudo", "url": "Liens des contenus"}

    column_filters = ("name",)

    @staticmethod
    def get_query() -> Query:
        return (
            Member.query.join(
                Subscription, Subscription.member_id == Member.id,
            )
            .filter(Subscription.campagne == "2023")
            .filter(Member.confirmed_departure.is_(False))
        )

    def get_count_query(self) -> Query:
        return self.get_query().with_entities(func.count(self.model.id))

    def format_url(self, context, model, name) -> Markup:
        return Markup(
            " ".join(
                '<a href="{url}" title="Link to member\'s platform">{url}</a>'.format(
                    url=word if word.startswith("http") else "https://" + word
                )
                if any(
                    ext in word
                    for ext in (
                        "http",
                        ".com",
                        ".fr",
                        ".tv",
                        ".org",
                        ".Science",
                    )
                )
                else word
                for word in re.split(" |\n", model.url)
            ),
        )

    column_formatters: ClassVar[dict[str, Callable]] = {
        "url": format_url,
    }

    @staticmethod
    def is_accessible() -> bool:
        return True


class Member2024ListView(Member2023ListView):
    @staticmethod
    def get_query() -> Query:
        return (
            Member.query.join(
                Subscription, Subscription.member_id == Member.id,
            )
            .filter(Subscription.campagne == "2024")
            .filter(Member.confirmed_departure.is_(False))
        )


class Member2025ListView(Member2023ListView):
    @staticmethod
    def get_query() -> Query:
        return (
            Member.query.join(
                Subscription, Subscription.member_id == Member.id,
            )
            .filter(Subscription.campagne == "2025")
            .filter(Member.confirmed_departure.is_(False))
        )
    
class Member2026ListView(Member2023ListView):
    @staticmethod
    def get_query() -> Query:
        return (
            Member.query.join(
                Subscription, Subscription.member_id == Member.id,
            )
            .filter(Subscription.campagne == "2026")
            .filter(Member.confirmed_departure.is_(False))
        )


class MemberToContact2022(CdsModelView):
    column_list = (
        "name",
        "email",
        "subscriptions",
        "up_to_date",
        "is_2026",
        "is_2025",
        "is_2024",
        "is_2023",
        "is_2022",
        "is_2021",
        "is_2020",
        "is_pre2019",
        "confirmed_departure",
        "mail_sent",
        "last_subscription",
    )

    column_details_list = (
        "name",
        "email",
        "subscriptions",
        "up_to_date",
        "is_2026",
        "is_2025",
        "is_2024",
        "is_2023",
        "is_2022",
        "is_2021",
        "is_2020",
        "is_pre2019",
        "confirmed_departure",
        "mail_sent",
        "last_subscription",
    )

    @staticmethod
    def get_query() -> Query:
        return Member.query.join(Subscription).filter(
            Member.subscriptions.any(Subscription.campagne == "2022"),
            ~Member.subscriptions.any(Subscription.campagne == "2023"),
            Member.confirmed_departure.is_(False),
        )

    def get_count_query(self) -> Query:
        return self.get_query().with_entities(
            func.count(func.distinct(self.model.id)),
        )

    def format_subscriptions(self, context, model: list[Subscription], name) -> Markup:
        return Markup(
            "<br>".join(
                '<a href="{url}" title="Link to Subscription">{subscription}</a>'.format(
                    url=url_for("subscription.details_view", id=s.id),
                    subscription=s.campagne,
                )
                for s in model.subscriptions
            ),
        )

    def format_last_subscription(self, context, model: Subscription, name) -> Markup:
        return Markup(
            '<a href="{url}" title="Link to Subscription">{subscription}</a>'.format(
                url=url_for("subscription.details_view", id=model.last_subscription.id),
                subscription=model.last_subscription.campagne,
            ),
        )

    column_formatters: ClassVar[dict[str, Callable]] = {
        "subscriptions": format_subscriptions,
        "last_subscription": format_last_subscription,
    }

    column_formatters_detail: ClassVar[dict[str, Callable]] = {
        "subscriptions": format_subscriptions,
        "last_subscription": format_last_subscription,
    }

    column_default_sort = "name"


class MemberToContact2021(MemberToContact2022):
    @staticmethod
    def get_query() -> Query:
        return Member.query.join(Subscription).filter(
            Member.subscriptions.any(Subscription.campagne == "2021"),
            ~Member.subscriptions.any(Subscription.campagne == "2022"),
            ~Member.subscriptions.any(Subscription.campagne == "2023"),
            Member.confirmed_departure.is_(False),
        )


class MemberToContact2020(MemberToContact2022):
    @staticmethod
    def get_query() -> Query:
        return Member.query.join(Subscription).filter(
            Member.subscriptions.any(Subscription.campagne == "2020"),
            ~Member.subscriptions.any(Subscription.campagne == "2021"),
            ~Member.subscriptions.any(Subscription.campagne == "2022"),
            ~Member.subscriptions.any(Subscription.campagne == "2023"),
            Member.confirmed_departure.is_(False),
        )


class MemberToContact2023(MemberToContact2022):
    page_size = 200

    @staticmethod
    def get_query() -> Query:
        return Member.query.join(Subscription).filter(
            Member.subscriptions.any(Subscription.campagne == "2023"),
            ~Member.subscriptions.any(Subscription.campagne == "2024"),
            Member.confirmed_departure.is_(False),
        )
