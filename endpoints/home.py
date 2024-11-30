from pathlib import Path

from flask import Blueprint, Response, current_app, render_template, send_from_directory
from flask_babel import gettext

home = Blueprint("home", __name__)


@home.route("/")
def index() -> str:
    return render_template("index.html")


@home.route("/camera")
def camera() -> str:
    user_image = Path("static") / "pic.jpg"
    return render_template(
        "camera.html", user_image=user_image, title=gettext("Camera"),
    )


@home.route("/CV")
def cv() -> Response:
    return send_from_directory(
        Path(current_app.root_path) / "static", "CV_Pierre_Rambourg_Fr_2023.pdf",
    )


@home.route("/ads.txt")
def ads() -> Response:
    return send_from_directory(
        Path(current_app.root_path) / "static", "ads.txt",
    )
