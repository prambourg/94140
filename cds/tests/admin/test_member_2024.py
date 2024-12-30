from flask.testing import FlaskClient
from sqlalchemy.orm.scoping import scoped_session


def test_member_list_2024_as_guest(
        client: FlaskClient,
        create_data: scoped_session,
    ) -> None:
    response = client.get("/liste_membre/")
    assert response.status_code == 200
    assert b"<title>Acc\xc3\xa8s refus\xc3\xa9</title>" not in response.data
    assert b"Caf\xc3\xa9 des Sciences - Liste des membres publique 2024 - Aeth&#39;s website" in response.data


def test_member_list_2024_as_user(
        client: FlaskClient,
        create_data: scoped_session,
        login_as_user,
    ) -> None:
    response = client.get("/liste_membre/")
    assert response.status_code == 200
    assert b"<title>Acc\xc3\xa8s refus\xc3\xa9</title>" not in response.data
    assert b"Caf\xc3\xa9 des Sciences - Liste des membres publique 2024 - Aeth&#39;s website" in response.data


def test_member_list_2024_as_admin(
        client: FlaskClient,
        create_data: scoped_session,
        login_as_admin,
    ) -> None:
    response = client.get("/liste_membre/")
    assert response.status_code == 200
    assert b"<title>Acc\xc3\xa8s refus\xc3\xa9</title>" not in response.data
    assert b"Caf\xc3\xa9 des Sciences - Liste des membres publique 2024 - Aeth&#39;s website" in response.data
