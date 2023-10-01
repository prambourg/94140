from conf import ENVIRONMENT

if ENVIRONMENT == "prod":
    this_file = "venv/bin/activate_this.py"
    exec(open(this_file).read(), {'__file__': this_file})

import os

from flask_admin import Admin
from flask import Flask, send_from_directory, render_template, request
from flask_pydantic import validate
from retry import retry
from sqlalchemy.exc import OperationalError

from admin import AethModelView
from admin.basket import BasketAdminView
from admin.order import HelloAssoView
from admin.product import ProductAdminView
from admin.purchase import PurchaseAdminView
from models.base import db
from models.measurement import Measurement
from models.basket import Basket
from models.product import Product
from models.purchase import Purchase
from models.shop import Shop
from models.cds.order import Order
from endpoints.home import home
from endpoints.youtube import youtube_blueprint, yt_urls
from schemas.order import OrderSchema

app = Flask(__name__)
app.app_context().push()
app.config.from_pyfile("conf.py")


def get_locale():
    return request.accept_languages.best_match(['de', 'fr', 'en'])


from flask_babel import Babel, gettext

babel = Babel(app, locale_selector=get_locale)

from flask_migrate import Migrate

migrate = Migrate(app, db, compare_server_default=True)
app.config["ENVIRONMENT"] = ENVIRONMENT

db.init_app(app)

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name="Aeth's website", template_mode='bootstrap3')
admin.add_view(AethModelView(Measurement, db.session))
admin.add_view(HelloAssoView(Order, db.session))

admin.add_view(BasketAdminView(Basket, db.session, category="Trésorerie"))
admin.add_view(AethModelView(Shop, db.session, category="Trésorerie"))
admin.add_view(ProductAdminView(Product, db.session, category="Trésorerie"))
admin.add_view(PurchaseAdminView(Purchase, db.session, category="Trésorerie"))

app.config["YOUTUBE_URLS"] = [(key, value) for key, value in yt_urls.items()]


@home.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@home.route("/ads.txt")
def ads():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "ads.txt"
    )


@home.route("/camera")
def camera():
    user_image = os.path.join('static', 'pic.jpg')
    return render_template('camera.html', user_image=user_image, title=gettext('Camera'))


@home.route("/CV")
def cv():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "CV_Pierre_Rambourg_Fr_2023.pdf"
    )


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html', title=gettext('Page non trouvée'))

"""from utils.hello_asso import construct


@home.route('/hello_asso', methods=["POST", ])
def hello_asso():
    return {"result": construct()}"""


@home.route('/populate_hello_asso', methods=["POST", ])
@validate()
@retry(OperationalError, tries=10, delay=1)
def populate_hello_asso(body: OrderSchema):
    if request.method == "POST" and Order.query.filter(Order.hello_asso_id == body.hello_asso_id).one_or_none() is None:
        order = Order(
            hello_asso_id=body.hello_asso_id,
            first_name=body.first_name,
            last_name=body.last_name,
            email=body.email,
            campagne=body.campagne,
            type=body.type,
            amount=body.amount,
            date=body.date,
            twitter=body.twitter,
            facebook=body.facebook,
            instagram=body.instagram,
            url=body.url,
            name=body.name,
        )
        try:
            db.session.add(order)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        return 201
    else:
        return 202


from endpoints.measurement import measurement_blueprint

app.register_blueprint(measurement_blueprint)
from endpoints.home import home

app.register_blueprint(home)
from endpoints.python import tutorial_blueprint

app.register_blueprint(tutorial_blueprint)

app.register_blueprint(youtube_blueprint)
