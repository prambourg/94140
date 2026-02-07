from sqlalchemy import select

from models.base import User
from repository.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        return self.session.execute(stmt).scalar_one_or_none()
