from __future__ import annotations

from sqlalchemy.orm import Mapped, relationship

from models.base import BaseModel, intpk


class Shop(BaseModel):
    id: Mapped[intpk]
    label: Mapped[str]
    city: Mapped[str]
    baskets: Mapped[list["Basket"]] = relationship(back_populates="shop", lazy=True)  # type: ignore  # noqa: F821, PGH003, UP037

    def __repr__(self) -> str:
        return f"<Shop l: {self.label}, c: {self.city}>"
