from __future__ import annotations

from flask import Blueprint, Response, current_app, jsonify, request
from sqlalchemy import func, select

from cds.models.member import Member
from models.base import db

members_blueprint = Blueprint("members_blueprint", __name__)


@members_blueprint.route(
    "/members/",
    methods=[
        "GET",
    ],
)
def get_members() -> tuple[Response, int]:
    """Retrieve a paginated list of members.

    Query Parameters:
        limit (int, optional): Maximum number of members to return.
        offset (int, optional): Number of members to skip.
        year (int, optional): Filter members by year.

    Returns:
        tuple[Response, int]: JSON response with member data and HTTP status code.

    """
    limit = request.args.get("limit", type=int)
    offset = request.args.get("offset", type=int)
    year = request.args.get("year", type=int)

    if limit is not None and limit < 0:
        return jsonify({"error": "Limit must be non-negative"}), 400
    if offset is not None and offset < 0:
        return jsonify({"error": "Offset must be non-negative"}), 400

    stmt = select(Member.name)
    if limit is not None:
        stmt = stmt.limit(limit)
    if offset is not None:
        stmt = stmt.offset(offset)

    try:
        members = db.session.execute(stmt).scalars().all()
        total_members = db.session.execute(select(func.count()).select_from(Member)).scalar()
    except Exception as e:
        current_app.logger.exception("An error occurred while retrieving members: %s")
        return jsonify({"error": "Internal server error"}), 500

    return jsonify({
        "members": members,
        "pagination": {"limit": limit, "offset": offset, "total": total_members},
    }), 200
