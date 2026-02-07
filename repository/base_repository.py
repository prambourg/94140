from sqlalchemy import select
from sqlalchemy.orm import Session

from models.base import BaseModel


class BaseRepository:
    def __init__(self, session: Session) -> None:  # noqa: D107
        self.session = session

    def get_by_id(self, entity: BaseModel, entity_id: int) -> BaseModel:
        # https://docs.sqlalchemy.org/en/20/orm/session_basics.html#get-by-primary-key
        return self.session.get(entity, entity_id)

    def get_all(self, entity: BaseModel) -> list[BaseModel]:
        stmt = select(entity)
        return self.session.execute(stmt).scalars().all()

    def save(self, entity_instance: BaseModel) -> BaseModel:
        self.session.add(entity_instance)
        self.session.commit()
        self.session.refresh(entity_instance)
        return entity_instance

    def delete(self, entity_instance: BaseModel) -> None:
        self.session.delete(entity_instance)
        self.session.commit()
