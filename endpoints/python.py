from flask import Blueprint, render_template
from flask_babel import gettext

tutorial_blueprint = Blueprint("tutorial_blueprint", __name__)


@tutorial_blueprint.route(
    "/python/",
    methods=[
        "GET",
    ],
)
def tutorial() -> str:
    return render_template(
        "python/base.html", title=gettext("Python tutorial"),
    )


@tutorial_blueprint.route(
    "/python/about/",
    methods=[
        "GET",
    ],
)
def about() -> str:
    return render_template(
        "python/about.html", title=gettext("Python tutorial - About"),
    )


@tutorial_blueprint.route(
    "/python/csv/",
    methods=[
        "GET",
    ],
)
def csv() -> str:
    return render_template(
        "python/csv.html", title=gettext("Python tutorial - CSV"),
    )


@tutorial_blueprint.route(
    "/python/retry/",
    methods=[
        "GET",
    ],
)
def retry() -> str:
    return render_template(
        "python/retry.html", title=gettext("Python tutorial - Retry"),
    )
