from sqlalchemy import select
from sqlalchemy.orm.scoping import scoped_session

from models.basket import Basket


def test_basket(create_data: scoped_session) -> None:
    basket = create_data.execute(select(Basket)).scalar_one()

    assert basket.shop is not None
    assert isinstance(basket.purchases, list)
    assert len(basket.purchases) == 1
    assert basket.total_price == 123456 / 100
