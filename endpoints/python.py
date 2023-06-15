from flask import Blueprint, render_template
from flask_babel import gettext

tutorial_blueprint = Blueprint('tutorial_blueprint', __name__)


@tutorial_blueprint.route("/python", methods=["GET", ])
def tutorial():
    return render_template("python.html", title=gettext('Python tutorial'))
