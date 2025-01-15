from __future__ import annotations

from datetime import datetime

from flask import Blueprint, Response, current_app, jsonify, render_template, request, url_for
from sqlalchemy import func, select

from cds.models.member import Member
from cds.models.subscription import Subscription
from models.base import db
from utils.datetime_tools import TIMEZONE

members_blueprint = Blueprint("members_blueprint", __name__)
current_year = int(datetime.now(tz=TIMEZONE).strftime("%Y"))

DEFAULT_LIMIT = 300


@members_blueprint.route(
    "/members/",
    methods=[
        "GET",
    ],
)
def get_members() -> tuple[Response, int]:
    """Retrieve a paginated and alphabetically sorted list of members.

    Query Parameters:
        limit (int, optional): Maximum number of members to return (non-negative). Defaults to 300.
        offset (int, optional): Number of members to skip (non-negative). Defaults to 0.
        year (int, optional): Filter members by campaign year. Defaults to the current year.

    Returns:
        tuple[Response, int]: JSON response containing:
            - members (list): List of member tuples (name, format_url), sorted alphabetically by name.
            - pagination (dict): Metadata about the pagination:
                - limit: The specified or default limit.
                - offset: The specified or default offset.
                - total: Total number of members for the specified year.
                - year: The campaign year being queried.

    """
    limit = request.args.get("limit", type=int) or DEFAULT_LIMIT
    offset = request.args.get("offset", type=int) or 0
    year = request.args.get("year", type=int) or current_year

    if limit < 0:
        return jsonify({"error": "Limit must be non-negative"}), 400
    if offset < 0:
        return jsonify({"error": "Offset must be non-negative"}), 400

    stmt = (
        select(Member)
        .join(Subscription)
        .filter(Subscription.campagne == str(year))
        .order_by(Member.name)
        .limit(limit)
        .offset(offset)
    )

    try:
        members = db.session.execute(stmt).scalars().all()
        total_members = db.session.execute(
            select(func.count()).select_from(
                select(Member)
                .join(Subscription)
                .filter(Subscription.campagne == str(year))
                .subquery(),
            ),
        ).scalar()

        members = [(member.name, member.format_url) for member in members]

        return jsonify({
            "members": members,
            "pagination": {"limit": limit, "offset": offset, "total": total_members, "year": year},
        }), 200
    except Exception:
        current_app.logger.exception("An error occurred while retrieving members: %s")
        return jsonify({"error": "Internal server error"}), 500


@members_blueprint.route("/liste_membres/")
def liste_membres() -> str:
    return render_template("liste_membres.html")
