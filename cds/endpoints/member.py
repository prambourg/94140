from __future__ import annotations

from datetime import datetime

from flask import Blueprint, Response, current_app, jsonify, request
from sqlalchemy import func, select

from cds.models.member import Member
from cds.models.subscription import Subscription
from models.base import db
from utils.datetime_tools import TIMEZONE

members_blueprint = Blueprint("members_blueprint", __name__)
current_year = int(datetime.now(tz=TIMEZONE).strftime("%Y"))

@members_blueprint.route(
    "/members/",
    methods=[
        "GET",
    ],
)
def get_members() -> tuple[Response, int]:
    """Retrieve a paginated list of members.

    Query Parameters:
        limit (int, optional): Maximum number of members to return (non-negative). Defaults to 100.
        offset (int, optional): Number of members to skip (non-negative). Defaults 0.
        year (int, optional): Filter members by campagne year. Defaults to the current year.

    Returns:
        tuple[Response, int]: JSON response containing:
            - members (list): List of member names.
            - pagination (dict): Metadata about the pagination.

    """
    limit = request.args.get("limit", type=int) or 100
    offset = request.args.get("offset", type=int) or 0
    year = request.args.get("year", type=int) or current_year

    if limit < 0:
        return jsonify({"error": "Limit must be non-negative"}), 400
    if offset < 0:
        return jsonify({"error": "Offset must be non-negative"}), 400

    stmt = (
        select(Member.name)
        .join(Subscription)
        .filter(Subscription.campagne == year)
        .limit(limit)
        .offset(offset)
    )

    try:
        members = db.session.execute(stmt).scalars().all()
        total_members = db.session.execute(
            select(func.count()).select_from(
                select(Member)
                .join(Subscription)
                .filter(Subscription.campagne == year)
                .subquery(),
            ),
        ).scalar()

        return jsonify({
           "members": members,
            "pagination": {"limit": limit, "offset": offset, "total": total_members, "year": year},
        }), 200
    except Exception:
        current_app.logger.exception("An error occurred while retrieving members: %s")
        return jsonify({"error": "Internal server error"}), 500
