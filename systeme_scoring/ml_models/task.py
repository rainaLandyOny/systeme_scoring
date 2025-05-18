from celery import shared_task
from django.utils import timezone
from .retrainer import retrain_all_models

import logging
logger = logging.getLogger(__name__)

@shared_task(bind=True)
def monthly_retraining(self):
    try:
        logger.info("Début du réentraînement mensuel")
        retrain_all_models()
        logger.info("Réentraînement terminé avec succès")
    except Exception as e:
        logger.error(f"Échec du réentraînement : {str(e)}")
        raise self.retry(exc=e)