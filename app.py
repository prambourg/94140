from conf import ENVIRONMENT

if ENVIRONMENT == "prod":
    this_file = "venv/bin/activate_this.py"
    exec(open(this_file).read(), {'__file__': this_file})

import os

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import Flask, send_from_directory, render_template, request

from models.base import db
from models.measurement import Measurement
from models.basket import Basket
from models.product import Product
from models.purchase import Purchase
from models.shop import Shop
from endpoints.home import home
from endpoints.youtube import youtube_blueprint, yt_urls

application = Flask(__name__)
application.config.from_pyfile("conf.py")


def get_locale():
    return request.accept_languages.best_match(['de', 'fr', 'en'])


from flask_babel import Babel, gettext
babel = Babel(application, locale_selector=get_locale)


from flask_migrate import Migrate
migrate = Migrate(application, db, compare_server_default=True)
application.config["ENVIRONMENT"] = ENVIRONMENT



db.init_app(application)

application.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(application, name='microblog', template_mode='bootstrap3')
admin.add_view(ModelView(Measurement, db.session))
from utils.init_db import models_app
for model in models_app:
    admin.add_view(ModelView(model, db.session))

application.config["YOUTUBE_URLS"] = [(key, value) for key, value in yt_urls.items()]


@home.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(application.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@home.route("/camera")
def camera():
    user_image = os.path.join('static', 'pic.jpg')
    return render_template('camera.html', user_image=user_image, title=gettext('Camera'))


@home.route("/CV")
def cv():
    return send_from_directory(
        os.path.join(application.root_path, "static"),
        "CV_Pierre_Rambourg_Fr_2023.pdf"
    )


@application.errorhandler(404)
def not_found(e):
    return render_template('404.html', title=gettext('Page non trouvée'))


from endpoints.measurement import measurement_blueprint
application.register_blueprint(measurement_blueprint)
from endpoints.home import home
application.register_blueprint(home)
from endpoints.python import tutorial_blueprint
application.register_blueprint(tutorial_blueprint)

application.register_blueprint(youtube_blueprint)
