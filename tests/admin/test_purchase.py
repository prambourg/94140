from flask.testing import FlaskClient
from sqlalchemy.orm.scoping import scoped_session

from tests.conftest import htmlify
from utils.strings import ACCESS_DENIED, TRESORERY_CATEGORY, WEBSITE_NAME


def test_purchase_admin_as_guest(
        client: FlaskClient,
        create_data: scoped_session,
    ) -> None:
    response = client.get("/purchase/")
    assert response.status_code == 200
    assert ACCESS_DENIED in response.data


def test_purchase_admin_as_user(
        client: FlaskClient,
        create_data: scoped_session,
        login_as_user,
    ) -> None:
    response = client.get("/purchase/")
    assert response.status_code == 200
    assert ACCESS_DENIED in response.data


def test_purchase_admin_as_admin(
        client: FlaskClient,
        create_data: scoped_session,
        login_as_admin,
    ) -> None:
    response = client.get("/purchase/")
    assert response.status_code == 200
    assert ACCESS_DENIED not in response.data
    assert htmlify(f"{TRESORERY_CATEGORY} - Purchase - {WEBSITE_NAME}") in response.data
