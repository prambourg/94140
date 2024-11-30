from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import BaseModel, intpk


class PurchaseUnits(Enum):
    KG = "Kg"
    CL = "Cl"
    L = "L"
    u = "u"
    NULL = None


class Purchase(BaseModel):
    id: Mapped[intpk]
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    product: Mapped["Product"] = relationship(back_populates="purchases", lazy=True)  # type: ignore  # noqa: F821, PGH003
    price: Mapped[int]
    weight: Mapped[float | None]
    unit: Mapped[str | None]
    basket_id: Mapped[int] = mapped_column(ForeignKey("basket.id"))
    basket: Mapped["Basket"] = relationship(back_populates="purchases", lazy=True)  # type: ignore  # noqa: F821, PGH003

    @property
    def normalized_price(self) -> float:
        if self.unit == PurchaseUnits.KG.value:
            price = int(self.price / self.weight) / 100
            print(f"{self.price} € - {self.weight} kg - {price} €/kg")
            return price
        if self.unit == PurchaseUnits.u.value:
            return int(self.price / self.weight) / 100
        return self.price

    def __repr__(self) -> str:
        return f"<{self.product.description}, b: {self.basket.label}, price: {self.price}>"
