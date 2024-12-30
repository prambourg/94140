from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class AethModelView(ModelView):
    can_view_details = True
    page_size = 100

    @staticmethod
    def is_accessible() -> bool:
        return (
            current_user.is_authenticated
            and current_user.username == "admin"
        )


class CdsModelView(AethModelView):
    @staticmethod
    def is_accessible() -> bool:
        return current_user.is_authenticated
