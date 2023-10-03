import os

SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', '')
SECRET_KEY = os.environ.get('SECRET_KEY', '')
ENVIRONMENT = os.environ.get('ENVIRONMENT', '')
FONT_AWESOME_URL = os.environ.get('FONT_AWESOME_URL', '')
ANALYTICS_ID = os.environ.get('ANALYTICS_ID', '')
ADSENSE_ID = os.environ.get('ADSENSE_ID', '')

HELLOASSO_TOKEN_URL = os.environ.get('HELLOASSO_TOKEN_URL', '')
HELLOASSO_CLIENT_ID = os.environ.get('HELLOASSO_CLIENT_ID', '')
HELLOASSO_CLIENT_SECRET = os.environ.get('HELLOASSO_CLIENT_SECRET', '')
HELLOASSO_ORGANIZATION_SLUG = os.environ.get('HELLOASSO_ORGANIZATION_SLUG', '')

CDS_SECRET_KEY = os.environ.get('CDS_SECRET_KEY', '')
# babel
# pybabel extract -F ./translations/babel.cfg -o ./translations/messages.pot .
# pybabel update -i ./translations/messages.pot -d translations -l en
# pybabel compile -d translations

