from sqlalchemy import select
from sqlalchemy.orm.scoping import scoped_session

from models.product import Product


def test_product(create_data: scoped_session) -> None:
    product = create_data.execute(select(Product)).scalar_one()
    assert isinstance(product.purchases, list)
    assert len(product.purchases) == 1
