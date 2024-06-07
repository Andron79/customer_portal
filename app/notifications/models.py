import logging
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.translation import gettext_lazy as _
from customer_dashboard.models import Company, CompanyType
from users.models import UserProfile

logger = logging.getLogger(__name__)


class Notification(models.Model):
    created_at = models.DateTimeField(
        verbose_name=_('Created at'),
        auto_now_add=True
    )

    company = models.ManyToManyField(
        Company,
        verbose_name=_('Companies'),
        blank=True
    )
    company_types = models.ManyToManyField(
        CompanyType,
        verbose_name=_('Companies Types'),
        blank=True
    )
    subject = models.CharField(
        verbose_name=_('Subject'),
        max_length=250,
        blank=False,
        null=False
    )
    text = RichTextUploadingField(
        verbose_name=_('Text'),
        blank=True,
        null=True
    )
    to_email = models.BooleanField(
        verbose_name=_('Send by email'),
        null=False
    )

    def __str__(self):
        return str(self.subject)

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _("Notifications")
        ordering = ('-created_at',)


class NotificationInstance(models.Model):
    profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )
    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        verbose_name=_('Notifications'),
        blank=True,
        related_name='notifications'
    )
    is_read = models.BooleanField(
        verbose_name=_('is_read'),
        null=False,
        blank=False,
        default=False
    )

    def __str__(self):
        return f'Notification Instance {self.pk}'

    class Meta:
        verbose_name = _('Notification Instance')
        verbose_name_plural = _("Notifications Instances")
