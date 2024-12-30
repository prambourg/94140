import os
from logging.config import dictConfig

from flask import Flask, Response, flash, redirect, render_template, request, url_for
from flask_babel import Babel, gettext
from flask_cors import CORS
from flask_login import LoginManager, login_required, login_user, logout_user
from sqlalchemy import select

from admin import init_admin
from cds.endpoints.hello_asso import hello_asso_blueprint
from endpoints.home import home
from endpoints.measurement import measurement_blueprint
from endpoints.python import tutorial_blueprint
from endpoints.youtube import YOUTUBE_URLS, youtube_blueprint
from models.base import User, db
from utils.hello_asso import process_from_scratch

DATABASES = {}
if "RDS_HOSTNAME" in os.environ:
    DATABASES = {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ["RDS_DB_NAME"],
        "USERNAME": os.environ["RDS_USERNAME"],
        "PASSWORD": os.environ["RDS_PASSWORD"],
        "HOSTNAME": os.environ["RDS_HOSTNAME"],
        "PORT": os.environ["RDS_PORT"],
    }


def get_locale() -> str:
    return request.accept_languages.best_match(["de", "fr", "en"])


def create_app() -> Flask:  # noqa: C901, PLR0915
    dictConfig(
            {
    "version": 1,
    "formatters": {
            "default": {
                        "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                    },
            "simpleformatter": {
                        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
    },
    "handlers":
    {
        "wsgi": {
        "class": "logging.StreamHandler",
        "formatter": "default",
                },
        "custom_handler": {
        "class": "logging.FileHandler",
        "formatter": "simpleformatter",
        "filename": "logs/WARN.log",
        "level": "WARN",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["wsgi", "custom_handler"],
    }})
    # EB looks for an "application" callable by default.
    application = Flask(__name__)
    application.app_context().push()

    CORS(application, resources={r"/*": {"origins": "*"}})
    Babel(application, locale_selector=get_locale)

    application.config["ENVIRONMENT"] = os.getenv("ENVIRONMENT")
    application.config["ADSENSE_ID"] = os.getenv("ADSENSE_ID")
    application.config["ANALYTICS_ID"] = os.getenv("ANALYTICS_ID")
    if application.config["ENVIRONMENT"] == "prod":
        application.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = f"postgresql://{DATABASES['USERNAME']}:{DATABASES['PASSWORD']}@{DATABASES['HOSTNAME']}:{DATABASES['PORT']}/{DATABASES['NAME']}"
    else:
        application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

    application.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }
    application.secret_key = "123456"  # noqa: S105

    db.init_app(application)
    db.create_all()
    if db.session.execute(select(User).where(User.username == "admin")).scalar_one_or_none() is None:
        user = User(username="admin", password=os.getenv("CDS_SECRET_KEY", "admin"))  # noqa: S106
        db.session.add(user)
        db.session.commit()

    init_admin(application)
    application.config["FLASK_ADMIN_SWATCH"] = "cerulean"
    application.config["YOUTUBE_URLS"] = list(YOUTUBE_URLS.items())

    login_manager = LoginManager()
    login_manager.login_view = "app.login"
    login_manager.init_app(application)

    @login_manager.user_loader
    def load_user(user_id: str) -> User:
        stmt = select(User).where(User.id == int(user_id))
        return db.session.execute(stmt).scalar_one()

    @application.errorhandler(404)
    def not_found(e) -> str:  # noqa: ANN001, ARG001
        return render_template("404.html", title=gettext("Page non trouvée"))

    @application.errorhandler(403)
    def forbidden(e) -> str:  # noqa: ANN001, ARG001
        return render_template("403.html", title=gettext("Accès refusé"))

    @application.route("/login")
    def login() -> str:
        return render_template("login.html")

    @application.route("/login", methods=["POST"])
    def login_post() -> Response:
        username = request.form.get("username")
        password = request.form.get("password")
        remember = bool(request.form.get("remember"))

        user = db.session.execute(select(User).where(User.username == username)).scalar_one()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or username != user.username or password != user.password:
            flash("Please check your login details and try again.")
            return redirect(url_for("login"))  # if the user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        return redirect(url_for("home.index"))

    @application.route("/logout")
    @login_required
    def logout() -> Response:
        logout_user()
        return redirect(url_for("home.index"))

    @application.route("/process_from_scratch", methods=["GET"])
    @login_required
    def get_process_from_scratch() -> Response:
        process_from_scratch()
        return redirect(url_for("home.index"))

    application.register_blueprint(measurement_blueprint)
    application.register_blueprint(home)
    application.register_blueprint(tutorial_blueprint)
    application.register_blueprint(youtube_blueprint)
    application.register_blueprint(hello_asso_blueprint)

    return application


application = create_app()
application.logger.warning("Application launched!")


if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
