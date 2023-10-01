from flask import request
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.filters import EnumFilterInList

from conf import CDS_SECRET_KEY, ENVIRONMENT
from models.cds.order import Order

CAMPAGNES = ((('valider-l-adhesion-au-cafe-des-sciences', '2'), 'pré_2020'),
             (('adhesion-2020-au-cafe-des-sciences', 'adhesion-2020-au-cafe-des-sciences-2'), '2020'),
             (('cotisation-aux-cafe-des-sciences-annee-2021', 'rattrapage-adhesion-2021-au-cafe-des-sciences-2'),
              '2021'),
             (('cotisation-2022-au-cafe-des-sciences', 'rattrapage-adhesion-2022'), '2022'),
             ('cotisation-2023-au-cafe-des-sciences', '2023'),
             ('2', 'don'))


class HelloAssoView(ModelView):
    column_filters = [EnumFilterInList(column=Order.campagne, name='Campagne', options=CAMPAGNES),
                      'name',
                      'first_name',
                      'last_name', ]
    can_create = False
    can_edit = False
    can_delete = False
    column_exclude_list = ['hello_asso_id', ]
    can_export = True
    column_default_sort = ('hello_asso_id', True)

    def is_accessible(self):
        return request.args.get('key', '') == CDS_SECRET_KEY or ENVIRONMENT == 'dev'