from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django_celery_beat.apps import BeatConfig


class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customer_portal'

    BeatConfig.verbose_name = _("Periodic Tasks")
