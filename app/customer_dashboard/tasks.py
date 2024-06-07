from celery import shared_task
from django.core.management import call_command
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def clean_db():
    call_command("clean_lost_files", )
