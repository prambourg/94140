import pytest
from sqlalchemy.orm.scoping import scoped_session

from cds.models.member import Member
from cds.models.subscription import Subscription
from tests.conftest import app, captured_templates, login_as_admin, login_as_user, session


@pytest.fixture
def session_with_members(session: scoped_session) -> scoped_session:
    member_1 = Member(name="name_1")
    session.add(member_1)
    member_2 = Member(name="name_2")
    session.add(member_2)
    member_3 = Member(name="name_3")
    session.add(member_3)
    member_4 = Member(name="name_4")
    session.add(member_4)
    member_5 = Member(name="name_5")
    session.add(member_5)
    member_6 = Member(name="name_6")
    session.add(member_6)

    session.commit()

    sub_1 = Subscription(campagne="2025", member_id=member_1.id)
    session.add(sub_1)
    sub_2 = Subscription(campagne="2025", member_id=member_2.id)
    session.add(sub_2)
    sub_3 = Subscription(campagne="2025", member_id=member_3.id)
    session.add(sub_3)
    sub_4 = Subscription(campagne="2025", member_id=member_4.id)
    session.add(sub_4)
    sub_5 = Subscription(campagne="2025", member_id=member_5.id)
    session.add(sub_5)
    sub_6 = Subscription(campagne="2024", member_id=member_5.id)
    session.add(sub_6)

    return session
