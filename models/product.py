from __future__ import annotations

from enum import Enum
from typing import Any

from sqlalchemy import Label, func, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, relationship

from models.base import BaseModel, db, intpk
from models.purchase import Purchase


class ProductCategory(Enum):
    ALIMENT = "Aliment"
    HYGIENE = "Hygiène"
    ALCOHOL = "Alcool"
    OTHER = "Autre"


class Product(BaseModel):
    id: Mapped[intpk]
    label: Mapped[str | None]
    description: Mapped[str | None]
    category: Mapped[str | None]
    glucide: Mapped[int | None]
    protide: Mapped[int | None]
    lipide: Mapped[int | None]
    sel: Mapped[int | None]
    fiber: Mapped[int | None]
    purchases: Mapped[list[Purchase]] = relationship(back_populates="product", lazy=True)
    barcode: Mapped[int | None]

    def __repr__(self) -> str:
        return f"<Product d: {self.description}>"

    @property
    def average_price(self) -> float:
        purchases = db.session.execute(
            select(Purchase).where(Purchase.product_id == self.id),
        ).scalars().all()
        return (
            int(sum(p.normalized_price * 100 for p in purchases) / len(purchases))
        ) / 100

    @hybrid_property
    def n_total(self) -> int:
        return len(self.purchase)

    @n_total.expression
    def n_total(self) -> Label[Any]:
        return (
            select(func.count(Purchase.id))
            .where(Purchase.product_id == self.id)
            .label("n_total")
        )
