from __future__ import annotations

from flask import Blueprint, Response, jsonify, request
from sqlalchemy import select

from cds.models.member import Member
from models.base import db

members_blueprint = Blueprint("members_blueprint", __name__)


@members_blueprint.route(
    "/members/",
    methods=[
        "GET",
    ],
)
def get_members() -> Response:
    limit = request.args.get("limit", type=int)
    offset = request.args.get("offset", type=int)
    year = request.args.get("year", type=int)

    stmt = select(Member)
    if limit is not None:
        stmt = stmt.limit(limit)
    if offset is not None:
        stmt = stmt.offset(offset)

    members = db.session.execute(stmt).scalars().all()
    members_data = [member.row2dict("name") for member in members]
    return jsonify(members_data)
