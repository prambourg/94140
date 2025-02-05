from sqlalchemy import ScalarResult
from sqlalchemy.orm import Session

from cds.models.member import Member
from cds.repository.member_repository import MemberRepository


class MemberService:
    def __init__(self, session: Session) -> None:  # noqa: D107
        self.member_repo = MemberRepository(session)

    def get_members(
            self,
            year: int | None = None,
            limit: int | None = None,
            offset: int | None = None,
        ) -> ScalarResult[Member]:
        return self.member_repo.get_members(year=year, limit=limit, offset=offset)

    def get_members_count(self, year: int | None = None) -> int:
        return self.member_repo.get_members_count(year=year)
