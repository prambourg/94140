import re

from flask import current_app
from markupsafe import Markup
from sqlalchemy import func, select

from cds.models.subscription import Subscription
from models.base import BaseModel, db


def reconciliation() -> None:
    i = 1
    subscription: Subscription
    while subscription := db.session.execute(
            select(Subscription).where(Subscription.member_id.is_(None)),
          ).scalars().first():
        print(
            f"let's go for {subscription.name} - {subscription.email} - {subscription.name} - {i}",
        )
        i += 1

        member = db.session.execute(
                    select(Member)
                    .where(func.lower(Member.last_name) == func.lower(subscription.last_name))
                    .where(Member.last_name != "")
                    .where(func.lower(Member.first_name) == func.lower(subscription.first_name))
                    .where(Member.first_name != ""),
                 ).scalars().first()
        if member is not None:
            print(
                f"{subscription.first_name} {subscription.last_name} found !",
            )

        if member is None:
            member = db.session.execute(
                        select(Member)
                        .where(func.lower(Member.name) == func.lower(subscription.name))
                        .where(Member.name != ""),
                     ).scalars().first()
            if member is not None:
                print(f"{subscription.name} found !")

        if member is None:
            member = db.session.execute(
                        select(Member)
                        .where(func.lower(Member.email) == func.lower(subscription.email)),
                     ).scalars().first()
            if member is not None:
                print(f"{subscription.email} found !")

        if member is None:
            print(
                f"{subscription.name} not found, creation in progress",
            )
            member = Member(
                name=subscription.name,
                first_name=subscription.first_name,
                last_name=subscription.last_name,
                email=subscription.email,
            )
            db.session.add(member)

        subscription.member_id = member.id
        member.email = (
            subscription.email or member.email
        )
        member.last_name = (
            subscription.last_name or member.last_name
        )
        member.first_name = (
            subscription.first_name or member.first_name
        )
        member.name = (
            subscription.name or member.name
        )
        db.session.add(subscription)
        db.session.commit()


class Member(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    website = db.Column(db.String(512))
    subscriptions = db.relationship(
        "Subscription", backref="member", lazy=True,
    )
    confirmed_departure = db.Column(
        db.Boolean, default=False, server_default="0", nullable=False,
    )
    mail_sent = db.Column(
        db.Boolean, default=False, server_default="0", nullable=False,
    )

    @property
    def up_to_date(self) -> bool:
        if self.subscriptions is None:
            return False
        return (
            any("2025" in s.campagne for s in self.subscriptions)
            or self.confirmed_departure
        )

    @property
    def is_2024(self) -> bool:
        if self.subscriptions is None:
            return False
        return any("2024" in s.campagne for s in self.subscriptions)

    @property
    def is_2023(self) -> bool:
        if self.subscriptions is None:
            return False
        return any("2023" in s.campagne for s in self.subscriptions)

    @property
    def is_2022(self) -> bool:
        if self.subscriptions is None:
            return False
        return any("2022" in s.campagne for s in self.subscriptions)

    @property
    def is_2021(self) -> bool:
        if self.subscriptions is None:
            return False
        return any("2021" in s.campagne for s in self.subscriptions)

    @property
    def is_2020(self) -> bool:
        if self.subscriptions is None:
            return False
        return any("2020" in s.campagne for s in self.subscriptions)

    @property
    def is_pre2019(self) -> bool:
        if self.subscriptions is None:
            return False
        return any("pré-2019" in s.campagne for s in self.subscriptions)

    @property
    def url(self) -> str:
        if self.website is not None:
            return self.website

        ordered_subscriptions: list[Subscription] = self.ordered_subscriptions

        while ordered_subscriptions:
            subscription = ordered_subscriptions.pop()
            if subscription.url not in {"None", None}:
                return subscription.url

        return ""

    @property
    def ordered_subscriptions(self) -> list[Subscription]:
        ordered_subscriptions_index = {
            "pré-2019": -1,
            "2020": 0,
            "2021": 1,
            "2022": 2,
            "2023": 3,
            "2024": 4,
            "2025": 5,
        }

        def foo(elem: Subscription) -> int:
            return ordered_subscriptions_index[elem.campagne]

        return sorted(self.subscriptions, key=foo)

    @property
    def last_subscription(self) -> Subscription:
        sorted_subscriptions: list[Subscription] = self.ordered_subscriptions
        return sorted_subscriptions.pop()

    @property
    def format_url(self) -> Markup:
        try:
            return " ".join(
                '<a href="{url}" title="Link to member\'s platform">{url}</a>'.format(
                    url=word if word.startswith("http") else "https://" + word,
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
                for word in re.split(" |\n", self.url)
            )
        except TypeError:
            current_app.logger.warning(
                {
                    "error": "TypeError",
                    "member": self.row2dict(),
                    "url": self.url,
                },
            )

    def __repr__(self) -> str:
        return f"<Member {self.name} ({self.first_name} {self.last_name})>"
