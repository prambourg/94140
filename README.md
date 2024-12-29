[![CodeQL](https://github.com/prambourg/94140/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/prambourg/94140/actions/workflows/github-code-scanning/codeql)[![Dependabot Updates](https://github.com/prambourg/94140/actions/workflows/dependabot/dependabot-updates/badge.svg)](https://github.com/prambourg/94140/actions/workflows/dependabot/dependabot-updates)[![Run Unit Tests](https://github.com/prambourg/94140/actions/workflows/pytest.yml/badge.svg)](https://github.com/prambourg/94140/actions/workflows/pytest.yml)

# 94140 Website

Ce repo contient le code source de https://www.94140.fr. C'est à la fois un bac à sable, une présentation de mes compétences et un bloc note.

Contient également la gestion des membres du Café des Sciences

# Commandes utiles
## AWS
Quelques commandes utiles dans un environnement AWS  
Après aws cli d'installé, actualiser les identifiants :
> aws sso login  
> init project  
> eb init  
> eb deploy

Pour créer une app
> eb create <app_name>  
> eb create --cfg flask-env-sc flask-env

Pour détruire une app
> eb terminate <flask-env>

Lancer l'app en local
> python application.py

Pour créer/détruire une BDD de SQLalchemy Flask
> db.create_all()  
> db.drop_all()

En SSH chez AWS :
- app localization : /var/app/current
- venv localisation : /var/app/venv/staging-LQM1lest/bin/activate

load env var en SSH pour les avoir et pouvoir lancer un shell flask:
> eb ssh  
> sudo su -  
> export $(cat /opt/elasticbeanstalk/deployment/env | xargs)

Pour réduire à une instance AWS et éviter des coûts trop importants :
> Rolling update type -> disabled

## Utilisation d'UV
Créer l'environnement virtuel depuis un uv.lock :
> uv sync

Lancer pytest avec l'environnement créé précédemment
> uv run pytest

## Utilisation de Git
Créer et changer de branche
> git checkout -b <branch_name>

Changer de branche
> git checkout <branch_name>

Supprimer une branche locale :
> git branch -d <branch_name>

Supprimer une branche distance :
> git branch -D <branch_name>

Actualiser la liste des branches distantes, par exemple après en avoir supprimé :
> git remote update origin --prune

Modifier les n derniers commits d'une branche (exemple pour les squash)
> git rebase -i HEAD~n  
> git push -f
