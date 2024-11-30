after aws cli installed, actualize credentials :
aws sso login

init project
eb init

deploy
eb create <app_name>
eb create --cfg flask-env-sc flask-env

destroy
eb terminate <flask-env>

launch locally
python application.py

SQLalchemy Flask
db.create_all()
db.drop_all()

app localization : /var/app/current
venv localisation : /var/app/venv/staging-LQM1lest/bin/activate

load env var in ssh:
eb ssh
sudo su -
export $(cat /opt/elasticbeanstalk/deployment/env | xargs)

Rolling update type -> disabled