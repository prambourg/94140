from flask.testing import FlaskClient
from sqlalchemy.orm.scoping import scoped_session


def test_member_list_2024_as_guest(
        client: FlaskClient,
    ) -> None:
    response = client.get("/liste_membres/")
    assert response.status_code == 200
    assert b"<title>Acc\xc3\xa8s refus\xc3\xa9</title>" not in response.data


def test_member_list_2024_as_user(
        client: FlaskClient,
        login_as_user,
    ) -> None:
    response = client.get("/liste_membres/")
    assert response.status_code == 200
    assert b"<title>Acc\xc3\xa8s refus\xc3\xa9</title>" not in response.data


def test_member_list_2024_as_admin(
        client: FlaskClient,
        login_as_admin,
    ) -> None:
    response = client.get("/liste_membres/")
    assert response.status_code == 200
    assert b"<title>Acc\xc3\xa8s refus\xc3\xa9</title>" not in response.data
