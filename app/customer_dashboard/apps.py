from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CustomerDashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customer_dashboard'
    verbose_name = _("Companies")
