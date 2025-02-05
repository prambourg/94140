from sqlalchemy import ScalarResult, func, select

from cds.models.member import Member
from cds.models.subscription import Subscription
from repository.base_repository import BaseRepository


class MemberRepository(BaseRepository):
    def get_members(self,
        year: int | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> ScalarResult[Member]:
        stmt = select(Member).join(Subscription).order_by(Member.name)

        if year is not None:
            stmt = stmt.filter(Subscription.campagne == str(year))

        if limit is not None:
            stmt = stmt.limit(limit)

        if offset is not None:
            stmt = stmt.offset(offset)

        return self.session.execute(stmt).scalars().all()

    def get_members_count(self, year: int | None = None) -> int:
        stmt = select(Member)

        if year is not None:
            stmt = stmt.join(Subscription).filter(Subscription.campagne == str(year))

        return self.session.execute(
            select(func.count()).select_from(stmt.subquery()),
        ).scalar()
