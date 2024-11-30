from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class AethModelView(ModelView):
    can_view_details = True
    page_size = 100

    def is_accessible(self) -> bool:
        return (
            current_user.is_authenticated
            and current_user.username == "admin"
        )


class CdsModelView(AethModelView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated
