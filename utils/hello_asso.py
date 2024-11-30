from __future__ import annotations

import datetime
import os
from typing import Any, Literal

from helloasso_api import HaApiV5
from sqlalchemy import select

from admin.subscription import CAMPAGNES_YEAR
from models.base import db
from models.cds.member import Member, reconciliation
from models.cds.subscription import Subscription

if os.getenv("ENVIRONMENT") is not None:
    hello_asso_api = HaApiV5(
        api_base="api.helloasso.com",
        client_id=os.getenv("HELLOASSO_CLIENT_ID"),
        client_secret=os.getenv("HELLOASSO_CLIENT_SECRET"),
    )


def process_custom_fields(data: list[dict[Any]]) -> dict[str, Any]:
    _d = {}
    for item in data:
        _d[item["name"]] = item["answer"]
    return {
        "twitter": _d.get("Twitter", ""),
        "facebook": _d.get("Facebook", ""),
        "instagram": _d.get("Instagram", ""),
        "url": _d.get("Lien vers votre contenu", "")
        or _d.get(
            "Lien vers le contenu agrégé au Café (ex : blog, chaîne YouTube)",
            "",
        ),
        "name": _d.get("Nom du contenu agrégé au Café", "")
        or _d.get("Nom de votre chaîne/Blog/Structure/etc.", "")
        or _d.get("Chaîne/Blog/Structure/etc.", ""),
    }


def create_subscription(data: dict[Any]) -> (tuple[Subscription, Literal[1]] | tuple[None, Literal[0]]):
    try:
        filtered_data = {
            "hello_asso_id": data["id"],
            "type": data["formType"],
            "last_name": data["payer"]["lastName"].capitalize().strip(),
            "first_name": data["payer"]["firstName"].capitalize().strip(),
            "email": data["payer"]["email"].strip(),
            "customFields": data["items"][0].get("customFields", []),
            "campagne": CAMPAGNES_YEAR.get(data["formSlug"], data["formSlug"]),
            "amount": data["amount"]["total"],
            "date": datetime.datetime.strptime(  # noqa: DTZ007
                data["date"][:19], "%Y-%m-%dT%H:%M:%S",
            ),
        }
        if (
            db.session.execute(
                select(Subscription)
                .where(Subscription.hello_asso_id == filtered_data["hello_asso_id"]),
            ).scalar_one_or_none()
            is None
            and filtered_data["type"] == "Membership"
        ):
            custom_fields = process_custom_fields(
                filtered_data["customFields"],
            )
            subscription = Subscription(
                hello_asso_id=filtered_data["hello_asso_id"],
                first_name=filtered_data["first_name"],
                last_name=filtered_data["last_name"],
                email=filtered_data["email"],
                campagne=filtered_data["campagne"],
                type=filtered_data["type"],
                amount=int(filtered_data["amount"]) / 100,
                date=filtered_data["date"],
                twitter=custom_fields["twitter"],
                facebook=custom_fields["facebook"],
                instagram=custom_fields["instagram"],
                url=custom_fields["url"],
                name=custom_fields["name"].capitalize().strip(),
            )
            db.session.add(subscription)
            return subscription, 1
    except KeyError:
        print(data)
    return None, 0


def build_db(page: int = 1, size: int = 20) -> tuple[int, int]:
    r = hello_asso_api.call(
        f"/v5/organizations/c-fetiers-des-sciences/orders?withDetails=true"
        f"&pageIndex={page}"
        f"&sortOrder=Asc"
        f"&pageSize={size}",
        method="GET",
    )
    datas = r.json()["data"]

    n = 0
    for data in datas:
        _, i = create_subscription(data)
        n += i
    db.session.commit()
    print(f"{n} entities added")
    print(f"{len(datas)} in this batch")
    return len(datas), n


def delete_subscriptions() -> None:
    db.session.query(Subscription).delete()
    db.session.commit()


def construct() -> int:
    batch_size = -1
    page = 1
    size = 100
    total = 0
    while batch_size != 0:
        batch_size, n_added = build_db(page, size)
        total += n_added
        page += 1
    return total


def process() -> None:
    construct()
    reconciliation()


def process_from_scratch() -> None:
    db.session.query(Subscription).delete()
    db.session.query(Member).delete()
    db.session.commit()
    process()
