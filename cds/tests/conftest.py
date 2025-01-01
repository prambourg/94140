import pytest
from sqlalchemy.orm.scoping import scoped_session

from cds.models.member import Member
from tests.conftest import app, login_as_admin, login_as_user, session


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

    session.commit()

    return session
