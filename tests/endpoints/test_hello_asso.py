import json
import os

from flask.testing import FlaskClient
from sqlalchemy.orm.scoping import scoped_session

from models.cds.member import Member
from models.cds.subscription import Subscription

payload = {
  "data": {
    "payer": {
      "email": "simplexpaleo@gmail.com",
      "country": "FRA",
      "firstName": "Alex",
      "lastName": "Bernardini",
    },
    "items": [
      {
        "payments": [
          {
            "id": 50978997,
            "shareAmount": 1000,
          },
        ],
        "name": "Tarif normal",
        "user": {
          "firstName": "Alex",
          "lastName": "Bernardini ",
        },
        "priceCategory": "Fixed",
        "customFields": [
          {
            "id": 3625645,
            "name": "Nom de votre chaîne/Blog/Structure/etc.",
            "type": "TextInput",
            "answer": "Simplex Paléo",
          },
          {
            "id": 3625646,
            "name": "Lien vers votre contenu",
            "type": "FreeText",
            "answer": "https://youtube.com/@simplexpaleo",
          },
        ],
        "qrCode": "MTEwMTQwMDg3OjYzODY3MjA5MjU1ODc3MDM1MQ==",
        "membershipCardUrl": "https://www.helloasso.com/associations/c-fetiers-des-sciences/adhesions/cotisation-2024-au-cafe-des-sciences/carte-adherent?cardId=110140087&ag=110140087",
        "tierDescription": "",
        "tierId": 10734361,
        "id": 110140087,
        "amount": 1000,
        "type": "Membership",
        "initialAmount": 1000,
        "state": "Processed",
      },
    ],
    "payments": [
      {
        "items": [
          {
            "id": 110140087,
            "shareAmount": 1000,
            "shareItemAmount": 1000,
          },
        ],
        "cashOutState": "Transfered",
        "paymentReceiptUrl": "https://www.helloasso.com/associations/c-fetiers-des-sciences/adhesions/cotisation-2024-au-cafe-des-sciences/paiement-attestation/110140087",
        "id": 50978997,
        "amount": 1000,
        "date": "2024-11-14T19:28:58.335735+01:00",
        "paymentMeans": "Card",
        "installmentNumber": 1,
        "state": "Authorized",
        "meta": {
          "createdAt": "2024-11-14T19:27:35.8770351+01:00",
          "updatedAt": "2024-11-14T19:28:58.3796258+01:00",
        },
        "refundOperations": [],
      },
    ],
    "amount": {
      "total": 1000,
      "vat": 0,
      "discount": 0,
    },
    "id": 110140087,
    "date": "2024-11-14T19:28:58.5309447+01:00",
    "formSlug": "cotisation-2024-au-cafe-des-sciences",
    "formType": "Membership",
    "organizationName": "C@FETIERS DES SCIENCES",
    "organizationSlug": "c-fetiers-des-sciences",
    "organizationType": "Association1901Rig",
    "organizationIsUnderColucheLaw": False,
    "meta": {
      "createdAt": "2024-11-14T19:27:35.8770351+01:00",
      "updatedAt": "2024-11-14T19:28:58.5343521+01:00",
    },
    "isAnonymous": False,
    "isAmountHidden": False,
  },
  "eventType": "Order",
}


def test_hello_asso_callback_no_token(client: FlaskClient, session: scoped_session) -> None:
    response = client.post(
        "/hello_asso",
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
    )
    assert response.get_json() == {"answer": "wrong token"}
    assert response.status_code == 401


def test_hello_asso_callback(client: FlaskClient, session: scoped_session) -> None:
    key_test = "foobar"
    os.environ["CDS_SECRET_KEY"] = key_test
    response = client.post(
        f"/hello_asso?token={key_test}",
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
    )
    assert response.get_json() == {"answer": "ok"}
    assert response.status_code == 201

    assert len(Member.query.all()) == 1
    assert len(Subscription.query.all()) == 1
