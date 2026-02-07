from sqlalchemy.orm import Session

from models.base import User
from repository.user_repository import UserRepository


class UserService:
    def __init__(self, session: Session) -> None:  # noqa: D107
        self.user_repo = UserRepository(session)

    def get_user_by_id(self, user_id: int) -> User:
        return self.user_repo.get_by_id(User, user_id)

    def get_user_by_username(self, username: str) -> User:
        return self.user_repo.get_by_username(username)

    def save_user(self, username: str, password: str) -> User:
        user = User(username=username, password=password)
        return self.user_repo.save(user)
