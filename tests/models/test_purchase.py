from sqlalchemy import select
from sqlalchemy.orm.scoping import scoped_session

from models.purchase import Purchase


def test_purchase(create_data: scoped_session) -> None:
    purchase = create_data.execute(select(Purchase)).scalar_one()
    assert purchase.product is not None
    assert purchase.basket is not None
