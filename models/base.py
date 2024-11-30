from __future__ import annotations

from typing import Annotated

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()
intpk = Annotated[int, mapped_column(primary_key=True)]


class BaseModel(db.Model):
    __abstract__ = True

    def row2dict(self) -> dict[str, str]:
        return {
            c.name: str(getattr(self, c.name)) for c in self.__table__.columns
        }


class User(UserMixin, BaseModel):
    id: Mapped[intpk]
    username: Mapped[str]
    password: Mapped[str]
