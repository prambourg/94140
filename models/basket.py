from __future__ import annotations

from datetime import datetime  # noqa: TCH003

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import BaseModel, intpk
from models.purchase import Purchase  # noqa: TCH001
from models.shop import Shop  # noqa: TCH001


class Basket(BaseModel):
    id: Mapped[intpk]
    label: Mapped[str]
    date: Mapped[datetime]
    shop_id: Mapped[int] = mapped_column(ForeignKey("shop.id"))
    shop: Mapped[Shop] = relationship(back_populates="baskets", lazy=True)
    purchases: Mapped[list[Purchase]] = relationship(back_populates="basket", lazy=True)

    def __repr__(self) -> str:
        return f"<Basket l: {self.label}, d: {self.date}, s: {self.shop_id}>"

    @property
    def total_price(self) -> float:
        return sum(p.price for p in self.purchases) / 100
