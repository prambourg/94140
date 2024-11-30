from sqlalchemy.orm.scoping import scoped_session

from models.measurement import Measurement


def test_session_fixture(session: scoped_session) -> None:
    assert len(Measurement.query.all()) == 0
