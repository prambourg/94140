from sqlalchemy.orm.scoping import scoped_session

from cds.models.subscription import Subscription


def test_subscription(session: scoped_session) -> None:
    sub_1 = Subscription(campagne="2025", member_id=1234)

    assert repr(sub_1) == f"<Subscription Campagne {sub_1.campagne} id {sub_1.id}>"
