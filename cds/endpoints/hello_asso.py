from __future__ import annotations

import os
from typing import Literal

from flask import Blueprint, current_app, request
from retry import retry
from sqlalchemy.exc import OperationalError

from cds.models.member import reconciliation
from cds.utils.hello_asso import create_subscription
from models.base import db

hello_asso_blueprint = Blueprint("hello_asso_blueprint", __name__)


@hello_asso_blueprint.route(
    "/hello_asso",
    methods=[
        "POST",
    ],
)
@retry(OperationalError, tries=10, delay=1)
def hello_asso_notification() -> tuple[dict[str, str], Literal[200, 201, 401]]:
    if request.args.get("token", "") != os.getenv("CDS_SECRET_KEY"):
        return {"answer": "wrong token"}, 401

    json = request.get_json()

    current_app.logger.warning(json)

    if json.get("eventType", "") != "Order":
        return {"answer": "ignored event"}, 200

    _, _ = create_subscription(json.get("data", {}))
    db.session.commit()
    reconciliation()

    return {"answer": "ok"}, 201
