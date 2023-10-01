import glob
import re
from datetime import datetime

from pypdf import PdfReader

from models.base import db
from models.basket import Basket
from models.product import Product
from models.purchase import Purchase, PurchaseUnits
from models.shop import Shop



def extract_date(text):
    date_pattern = "[0-9]{1,2}\\/[0-9]{1,2}\\/[0-9]{4}"
    date = re.findall(date_pattern, text)
    if len(date) != 1:
        print('are you sure for the date ?!')
        raise
    print(date[0])
    return date[0].split('/')


def extract_purchases(text):
    purchases = text.split('TVAProduit QTE x P.U. Montant €\n')[1] \
        .split('\nTotal à payer')[0] \
        .split('\nTotal avant remises')[0] \
        .replace('5.5%', '') \
        .replace('20.0%', '') \
        .replace('immédiate', '1') \
        .split('\n')
    purchases = list(filter(lambda x: (x.startswith('5.5%') or x.startswith('20.0%') or x.startswith('Remise immédiate')), text.split('Total à payer')[0].split('\n')))
    purchases = [p.replace('5.5%', '').replace('20.0%', '').replace('immédiate', '1') for p in purchases]
    x_purchases = [p.rsplit(' ', 4) for p in purchases]
    process_purchases = [{'name': p[0], 'price': p[-1], 'n': p[1]} for p in x_purchases]
    return process_purchases


def find_or_create_product(label):
    product = Product.query.filter(Product.label == label).one_or_none()
    if product is None:
        product = Product(label=label)
        db.session.add(product)
        db.session.commit()
        print(f'Product {product.label} created !')
    else:
        print(f'Product {product.label} exists already !')
    return product


def find_or_create_shop(label):
    shop = Shop.query.filter(Shop.label == label).one_or_none()
    if shop is None:
        shop = Shop(label=label)
        db.session.add(shop)
        db.session.commit()
        print(f'Shop {shop.label} created !')
    else:
        print(f'Shop {shop.label} exists already !')
    return shop


def process(path):
    reader = PdfReader(path)
    text = ''
    for page in reader.pages:
        text += page.extract_text() + '\n'

    if 'MARKET MONTREUIL COEUR DE VILLE' in text:
        shop_name = 'MARKET MONTREUIL COEUR DE VILLE'
    elif 'LE MANS' in text:
        shop_name = 'LE MANS'
    else:
        raise

    d, m, y = extract_date(text)
    purchases = extract_purchases(text)

    shop = find_or_create_shop(shop_name)
    basket = Basket(label=f'Courses {d}/{m}/{y}',
                    date=datetime(int(y), int(m), int(d)),
                    shop_id=shop.id)
    db.session.add(basket)
    db.session.commit()

    for p in purchases:
        product = find_or_create_product(p['name'])
        purchase = Purchase(product_id=product.id,
                            price=int(float(p['price'])*100),
                            weight=p['n'],
                            unit=PurchaseUnits.u.value,
                            basket_id=basket.id,)
        db.session.add(purchase)
    db.session.commit()


def process_all():
    for path in glob.glob("*.pdf"):
        process(path)