from sqlalchemy import select
from sqlalchemy.orm.scoping import scoped_session

from models.shop import Shop


def test_basket(create_data: scoped_session) -> None:
    shop = create_data.execute(select(Shop)).scalar_one()

    assert shop.label
    assert shop.city
    assert isinstance(shop.baskets, list)
    assert len(shop.baskets) == 1
