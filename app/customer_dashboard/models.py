from django.db import models
from django.utils.translation import gettext_lazy as _

from customer_dashboard.validators import validate_digit


class BaseModel(models.Model):
    created_at = models.DateField(
        verbose_name=_("Created at"),
        auto_now_add=True
    )
    updated_at = models.DateField(
        verbose_name=_("Updated at"),
        auto_now=True
    )

    class Meta:
        abstract = True


class CompanyType(models.Model):
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=100,
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = _('Company Type')
        verbose_name_plural = _('Companies Types')


class Company(BaseModel):
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=100,
        unique=True,
        blank=False,
        null=False
    )
    inn = models.CharField(
        max_length=12,
        verbose_name=_('INN'),
        blank=False,
        null=True,
        validators=[validate_digit]
    )
    kpp = models.CharField(
        max_length=9,
        verbose_name=_('KPP'),
        blank=False,
        null=True,
        validators=[validate_digit]
    )
    company_type = models.ForeignKey(
        CompanyType,
        verbose_name=_('Company Type'),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='companies'
    )
    max_num_company_users = models.PositiveSmallIntegerField(
        verbose_name=_('Company Users Limit'),
        default=20,
        blank=False,
        null=False
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')
        constraints = [
            models.UniqueConstraint(fields=['inn', 'kpp'], name='uniq_company_key')
        ]
