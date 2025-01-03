import pytest
from sqlalchemy.orm.scoping import scoped_session

from cds.models.member import Member
from cds.models.subscription import Subscription
from tests.conftest import app, captured_templates, login_as_admin, login_as_user, session  # noqa: F401

members_data = [
    {
        "name": f"foo_{i}",
        "email": f"mail_{i}",
        "first_name": f"first_name_{i}",
        "last_name": f"last_name_{i}",
        "website": f"website_{i}",
    }
    for i in range(5)
]


def create_members_bundle(session_db: scoped_session, year: int = 2025, nb_member: int = 5) -> None:
    members_data = [
        {
            "name": f"foo_{year}_{i}",
            "email": f"mail_{year}_{i}",
            "first_name": f"first_name_{year}_{i}",
            "last_name": f"last_name_{year}_{i}",
            "website": f"website_{year}_{i}",
        }
        for i in range(nb_member)
    ]

    members = [Member(**member) for member in members_data]

    for member in members:
        session_db.add(member)
    session_db.commit()

    for index, member in enumerate(members):
        sub = Subscription(hello_asso_id=f"index_{year}_{index}", campagne=year, member_id=member.id)
        session_db.add(sub)

    session_db.commit()


@pytest.fixture
def session_with_members(session: scoped_session) -> scoped_session:
    create_members_bundle(session_db=session, year=2025, nb_member=5)
    create_members_bundle(session_db=session, year=2024, nb_member=1)

    return session
