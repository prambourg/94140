from flask.testing import FlaskClient
from sqlalchemy.orm.scoping import scoped_session

from models.cds.subscription import Subscription
from tests.conftest import htmlify
from utils.strings import ACCESS_DENIED, CDS_CATEGORY, WEBSITE_NAME


def test_subscription_admin_as_guest(
        client: FlaskClient,
        session: scoped_session,
    ) -> None:
    subscription = Subscription()
    session.add(subscription)
    session.commit()
    response = client.get("/subscription/")
    assert response.status_code == 200
    assert ACCESS_DENIED in response.data


def test_subscription_admin_as_user(
        client: FlaskClient,
        session: scoped_session,
        login_as_user,
    ) -> None:
    subscription = Subscription()
    session.add(subscription)
    session.commit()
    response = client.get("/subscription/")
    assert response.status_code == 200
    assert ACCESS_DENIED not in response.data
    assert htmlify(f"{CDS_CATEGORY} - Historique adhésions - {WEBSITE_NAME}") in response.data


def test_subscription_admin_as_admin(
        client: FlaskClient,
        session: scoped_session,
        login_as_admin,
    ) -> None:
    subscription = Subscription()
    session.add(subscription)
    session.commit()
    response = client.get("/subscription/")
    assert response.status_code == 200
    assert ACCESS_DENIED not in response.data
    assert htmlify(f"{CDS_CATEGORY} - Historique adhésions - {WEBSITE_NAME}") in response.data
