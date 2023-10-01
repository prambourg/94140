from flask_admin.contrib.sqla import ModelView

from conf import ENVIRONMENT


class AethModelView(ModelView):
    can_view_details = True
    page_size = 100

    def is_accessible(self):
        return ENVIRONMENT == 'dev'

