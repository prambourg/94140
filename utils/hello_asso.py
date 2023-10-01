import datetime
import json

import requests
from helloasso_api import HaApiV5

from conf import HELLOASSO_CLIENT_ID, HELLOASSO_CLIENT_SECRET
from models.base import db
from models.cds.order import Order

hello_asso_api = HaApiV5(
    api_base='api.helloasso.com',
    client_id=HELLOASSO_CLIENT_ID,
    client_secret=HELLOASSO_CLIENT_SECRET,
)


def process_custom_fields(data):
    _d = {}
    for item in data:
        _d[item["name"]] = item["answer"]
    d = {}
    d['twitter'] = _d.get('Twitter', '')
    d['facebook'] = _d.get('Facebook', '')
    d['instagram'] = _d.get('Instagram', '')
    d['url'] = _d.get('Lien vers votre contenu', '') or _d.get('Lien vers le contenu agrégé au Café (ex : blog, chaîne YouTube)', '')
    d['name'] = _d.get('Nom du contenu agrégé au Café', '') or _d.get('Nom de votre chaîne/Blog/Structure/etc.', '') or _d.get('Chaîne/Blog/Structure/etc.', '')
    return d


def build_db(page: int = 1, size: int = 20):
    r = hello_asso_api.call(f'/v5/organizations/c-fetiers-des-sciences/orders?withDetails=true'
                            f'&pageIndex={page}'
                            f'&sortOrder=Asc'
                            f'&pageSize={size}',
                            method="GET")
    datas = r.json()['data']

    n = 0
    for data in datas:
        try:
            filtered_data = {'hello_asso_id': data['id'],
                             'type': data['formType'],
                             'last_name': data['payer']['lastName'],
                             'first_name': data['payer']['firstName'],
                             'email': data['payer']['email'],
                             'customFields': data['items'][0].get('customFields',[]),
                             'campagne': data['formSlug'],
                             'amount': data['amount']['total'],
                             'date': datetime.datetime.strptime(data['date'][:19],'%Y-%m-%dT%H:%M:%S')}
            if Order.query.filter(Order.hello_asso_id == filtered_data['hello_asso_id']).one_or_none() is None \
                    and 'Membership' == filtered_data['type']:
                custom_fields = process_custom_fields(filtered_data['customFields'])
                order = Order(hello_asso_id=filtered_data['hello_asso_id'],
                              first_name=filtered_data['first_name'],
                              last_name=filtered_data['last_name'],
                              email=filtered_data['email'],
                              campagne=filtered_data['campagne'],
                              type=filtered_data['type'],
                              amount=int(filtered_data['amount'])/100,
                              date=filtered_data['date'],
                              twitter=custom_fields['twitter'],
                              facebook=custom_fields['facebook'],
                              instagram=custom_fields['instagram'],
                              url=custom_fields['url'],
                              name=custom_fields['name'],)
                db.session.add(order)
                n += 1
        except KeyError:
            print(data)
            return 0
    db.session.commit()
    print(f'{n} entities added')
    print(f'{len(datas)} in this batch')
    return len(datas), n


def delete_orders():
    db.session.query(Order).delete()
    db.session.commit()


def construct():
    r = -1
    page = 1
    size = 100
    total = 0
    while r != 0:
        r, n = build_db(page, size)
        total += n
        page += 1
    return total


def send_data_to_live():
    orders = Order.query.filter().all()
    headers = {'Content-Type': 'application/json'}
    o: Order
    for o in orders:
        body = json.dumps(o.row2dict())
        r = requests.post('https://94140.fr/populate_hello_asso', data=body, headers=headers)
        print(r.status_code)
