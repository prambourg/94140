from flask_admin import Admin

from cds.admin.member import (
    Member2023ListView,
    Member2024ListView,
    Member2025ListView,
    Member2026ListView,
    MemberToContact2020,
    MemberToContact2021,
    MemberToContact2022,
    MemberToContact2023,
    MemberView,
)
from cds.admin.subscription import HelloAssoView
from cds.models.member import Member
from cds.models.subscription import Subscription
from models.base import db
from utils.strings import CDS_CATEGORY


def init_cds_admin(admin: Admin) -> None:
    admin.add_view(
        HelloAssoView(
            Subscription,
            db.session,
            name="Historique adhésions",
            category=CDS_CATEGORY,
        ),
    )
    admin.add_view(
        Member2023ListView(
            Member,
            db.session,
            name="Liste des membres publique 2023",
            endpoint="liste_membres_2023",
            category=CDS_CATEGORY,
        ),
    )
    admin.add_view(
        Member2024ListView(
            Member,
            db.session,
            name="Liste des membres publique 2024",
            endpoint="liste_membres_2024",
            category=CDS_CATEGORY,
        ),
    )
    admin.add_view(
        Member2025ListView(
            Member,
            db.session,
            name="Liste des membres publique 2025",
            endpoint="liste_membres_2025",
            category=CDS_CATEGORY,
        ),
    )
    admin.add_view(
        Member2026ListView(
            Member,
            db.session,
            name="Liste des membres publique 2026",
            endpoint="liste_membres_2026",
            category=CDS_CATEGORY,
        ),
    )
    admin.add_view(
        MemberView(
            Member,
            db.session,
            name="Liste des membres détaillée",
            category=CDS_CATEGORY,
        ),
    )
    admin.add_view(
        MemberToContact2023(
            Member,
            db.session,
            name="A relancer 2023",
            endpoint="membresRelance2023",
            category=CDS_CATEGORY,
        ),
    )
    admin.add_view(
        MemberToContact2022(
            Member,
            db.session,
            name="A relancer 2022",
            endpoint="membresRelance2022",
            category=CDS_CATEGORY,
        ),
    )
    admin.add_view(
        MemberToContact2021(
            Member,
            db.session,
            name="A relancer 2021",
            endpoint="membresRelance2021",
            category=CDS_CATEGORY,
        ),
    )
    admin.add_view(
        MemberToContact2020(
            Member,
            db.session,
            name="A relancer 2020",
            endpoint="membresRelance2020",
            category=CDS_CATEGORY,
        ),
    )
