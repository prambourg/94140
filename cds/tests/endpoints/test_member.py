import pytest
from flask.testing import FlaskClient
from sqlalchemy.orm.scoping import scoped_session


@pytest.mark.parametrize(
        ("limit", "offset", "expected"),
        [
            (None, None, 5),
            (0, 0, 0),
            (2, 0, 3),
            (2, 2, 1),
            (0, 5, 0),
        ])
def test_get_members(
    client: FlaskClient,
    session_with_members: scoped_session,
    limit: str,
    offset: str | None,
    expected: int | None,
) -> None:
    url = "/members/?"
    if limit is not None:
        url += f"limit={limit}&"
    if offset is not None:
        url += f"offset={offset}"

    response = client.get(
        url,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 200
    assert len(response.json) == expected