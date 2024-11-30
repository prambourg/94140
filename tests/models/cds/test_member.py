import pytest
from sqlalchemy.orm.scoping import scoped_session

from models.cds.member import Member, reconciliation
from models.cds.subscription import Subscription

sub_base = {
    "first_name": "Pierre",
    "last_name": "Rambourg",
    "name": "yt_channel_name",
    "email": "pierre.rambourg@foobar.com",
}


sub_same_name = Subscription(
    first_name="foo",
    last_name="bar",
    name="yt_channel_name",
    email="foo.bar@foobar.com",
)

sub_same_name_different_case = Subscription(
    first_name="foo",
    last_name="bar",
    name="Yt_cHanNel_nAme",
    email="foo.bar@foobar.com",
)

sub_same_first_last_name = Subscription(
    first_name="Pierre",
    last_name="Rambourg",
    name="yt_foobar_name",
    email="foobarfoobar@foobar.com",
)

sub_same_first_last_name_different_case = Subscription(
    first_name="PiErRe",
    last_name="RaMboUrg",
    name="yt_foobar_name",
    email="foobarfoobar@foobar.com",
)

sub_same_mail = Subscription(
    first_name="Pedro",
    last_name="Rambo",
    name="yt_barfoo_name",
    email="pierre.rambourg@foobar.com",
)

sub_same_mail_different_case = Subscription(
    first_name="Pedro",
    last_name="Rambo",
    name="yt_barfoo_name",
    email="PieRre.raMboUrg@foObar.com",
)


@pytest.mark.parametrize(
        "new_sub",
        [
            sub_same_name,
            sub_same_name_different_case,
            sub_same_first_last_name,
            sub_same_first_last_name_different_case,
            sub_same_mail,
            sub_same_mail_different_case,
        ],
)
def test_reconciliation(session: scoped_session, new_sub: Subscription) -> None:
    base = Subscription(**sub_base)
    session.add(base)
    session.commit()

    member = Member(
        name=base.name,
        first_name=base.first_name,
        last_name=base.last_name,
        email=base.email,
    )
    session.add(member)

    session.add(new_sub)

    reconciliation()

    assert new_sub.member_id == member.id == base.member_id
    assert member.first_name == new_sub.first_name
    assert member.last_name == new_sub.last_name
    assert member.name == new_sub.name
    assert member.email == new_sub.email


def test_sub_same_name_missing_data(session: scoped_session) -> None:
    base = Subscription(**sub_base)
    session.add(base)
    session.commit()

    member = Member(
        name=base.name,
        first_name=base.first_name,
        last_name=base.last_name,
        email=base.email,
    )
    session.add(member)
    sub_same_name_missing_data = Subscription(
        name="yt_channel_name",
    )
    session.add(sub_same_name_missing_data)

    reconciliation()

    assert sub_same_name_missing_data.member_id == member.id == base.member_id
    assert member.first_name == base.first_name
    assert member.last_name == base.last_name
    assert member.name == sub_same_name_missing_data.name
    assert member.email == base.email


def test_sub_same_first_last_name(session: scoped_session) -> None:
    base = Subscription(**sub_base)
    session.add(base)
    session.commit()

    member = Member(
        name=base.name,
        first_name=base.first_name,
        last_name=base.last_name,
        email=base.email,
    )
    session.add(member)
    sub_same_first_last_name_missing_data = Subscription(
        first_name="Pierre",
        last_name="Rambourg",
    )
    session.add(sub_same_first_last_name_missing_data)

    reconciliation()

    assert sub_same_first_last_name_missing_data.member_id == member.id == base.member_id
    assert member.first_name == sub_same_first_last_name_missing_data.first_name
    assert member.last_name == sub_same_first_last_name_missing_data.last_name
    assert member.name == base.name
    assert member.email == base.email


def test_sub_same_mail_missing_data(session: scoped_session) -> None:
    base = Subscription(**sub_base)
    session.add(base)
    session.commit()

    member = Member(
        name=base.name,
        first_name=base.first_name,
        last_name=base.last_name,
        email=base.email,
    )
    session.add(member)
    sub_same_mail_missing_data = Subscription(
        email="pierre.rambourg@foobar.com",
    )
    session.add(sub_same_mail_missing_data)

    reconciliation()

    assert sub_same_mail_missing_data.member_id == member.id == base.member_id
    assert member.first_name == base.first_name
    assert member.last_name == base.last_name
    assert member.name == base.name
    assert member.email == sub_same_mail_missing_data.email
