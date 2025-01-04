import pytest
from sqlalchemy.orm.scoping import scoped_session

from cds.models.member import Member, reconciliation
from cds.models.subscription import Subscription
from cds.tests.conftest import create_members_bundle

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


def test_member_properties(session: scoped_session) -> None:
    create_members_bundle(session, 2025, 1)
    member: Member = session.query(Member).first()
    assert member.up_to_date is True
    assert member.is_2024 is False
    assert member.is_2023 is False
    assert member.is_2022 is False
    assert member.is_2021 is False
    assert member.is_2020 is False
    assert member.is_pre2019 is False
    assert member.url == "website_2025_0"
    assert member.ordered_subscriptions == [*member.subscriptions]
    assert member.last_subscription == member.subscriptions[0]
    assert member.format_url == "website_2025_0"
    assert repr(member) == f"<Member {member.name} ({member.first_name} {member.last_name})>"


def test_member_url(session: scoped_session) -> None:
    create_members_bundle(session, 2022, 1)
    member: Member = session.query(Member).first()
    sub_2020: Subscription = session.query(Subscription).first()

    member.website = "member_foobar"
    sub_2020.url = "sub_2020_foobar"

    assert member.url == "member_foobar"

    member.website = None
    assert member.url == "sub_2020_foobar"

    sub_2025 = Subscription(hello_asso_id="foobar_id", campagne="2025", url="sub_2025_foobar", member_id=member.id)
    session.add(sub_2025)
    session.commit()

    assert member.url == "sub_2025_foobar"


def test_member_subscriptions(session: scoped_session) -> None:
    create_members_bundle(session, 2020, 1)
    member: Member = session.query(Member).first()
    sub_2020: Subscription = session.query(Subscription).first()

    assert member.is_2020 is True
    assert member.up_to_date is False

    sub_2025 = Subscription(hello_asso_id="foobar_id", campagne="2025", member_id=member.id)
    session.add(sub_2025)
    session.commit()

    assert member.ordered_subscriptions == [sub_2020, sub_2025]
    assert member.last_subscription == sub_2025
    assert member.is_2020 is True
    assert member.up_to_date is True
