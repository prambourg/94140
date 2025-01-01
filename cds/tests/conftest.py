import pytest
from sqlalchemy.orm.scoping import scoped_session

from cds.models.member import Member
from tests.conftest import app, session


@pytest.fixture
def session_with_members(session: scoped_session) -> scoped_session:
    member_1 = Member()
    session.add(member_1)
    member_2 = Member()
    session.add(member_2)
    member_3 = Member()
    session.add(member_3)
    member_4 = Member()
    session.add(member_4)
    member_5 = Member()
    session.add(member_5)

    session.commit()

    return session