"""Scheduler pour les tâches automatiques périodiques."""
from __future__ import annotations

import logging
import os

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask import Flask

from cds.utils.hello_asso import process

logger = logging.getLogger(__name__)


def sync_members_job(app: Flask) -> None:
    """Tâche de synchronisation des membres HelloAsso.
    
    Args:
        app: Instance Flask pour le contexte de l'application.
    
    """
    with app.app_context():
        try:
            logger.info("Début de la synchronisation automatique HelloAsso")
            process()
            logger.info("Synchronisation automatique HelloAsso réussie")
        except Exception as e:
            logger.exception("Erreur lors de la synchronisation automatique: %s", str(e))


def init_scheduler(app: Flask) -> BackgroundScheduler | None:
    """Initialize le scheduler pour les tâches périodiques.
    
    Args:
        app: Instance Flask.
        
    Returns:
        Le scheduler initialisé ou None si l'environnement ne nécessite pas de scheduler.
    
    """
    # Ne démarre le scheduler que si l'environnement est configuré
    if os.getenv("ENVIRONMENT") is None:
        logger.warning("Scheduler désactivé : variable ENVIRONMENT non définie")
        return None
    
    scheduler = BackgroundScheduler(daemon=True)
    
    # Synchronisation toutes les heures à la minute 0
    scheduler.add_job(
        func=lambda: sync_members_job(app),
        trigger=CronTrigger(minute=0),  # Toutes les heures
        id="sync_members_hourly",
        name="Synchronisation HelloAsso (toutes les heures)",
        replace_existing=True,
    )
    
    scheduler.start()
    logger.info("Scheduler démarré : synchronisation HelloAsso toutes les heures")
    
    return scheduler
