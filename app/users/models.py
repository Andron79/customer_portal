import logging
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError

from django.db import models
from django.http import Http404

from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from kombu.exceptions import OperationalError

from customer_dashboard.models import Company
from .managers import CustomUserManager
from .tasks import send_verification_email

logger = logging.getLogger(__name__)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _('email address'),
        unique=True
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_("Is staff")
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name=_("Is active")
    )
    date_joined = models.DateTimeField(
        _('registration date'),
        default=timezone.now
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class EmailVerificationToken(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='email_verification_token'
    )
    verification_uuid = models.UUIDField(
        default=uuid.uuid4,
        null=True,
        verbose_name=_("Token")
    )

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = _('Token')
        verbose_name_plural = _('Tokens')


class UserProfile(models.Model):
    COMPANY_ADMIN = 1
    COMPANY_EMPLOYEE = 2

    ROLE_CHOICES = (
        (COMPANY_ADMIN, _('Company Admin')),
        (COMPANY_EMPLOYEE, _('Company Employee')),
    )
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    name = models.CharField(
        verbose_name=_('Name'),
        max_length=100,
        blank=False,
        null=False
    )
    company = models.ForeignKey(
        Company,
        verbose_name=_('Company'),
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES,
        null=False,
        blank=False,
        default=1
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-user__date_joined']
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def clean(self, *args, **kwargs):
        super(UserProfile, self).clean()
        if not self.name:
            raise ValidationError(_('Not Name'))
        if not self.company_id:
            raise ValidationError(_('Not Company'))
        if not self.role:
            raise ValidationError(_('Not role'))

    def get_absolute_url(self):
        return reverse('user-profile', args=[str(self.id)])


def generate_token_and_send_verification_email(user_id: int):
    user_token = EmailVerificationToken.objects.update_or_create(
        user_id=user_id
    )[0]
    try:
        send_verification_email.delay(
            user_id=user_id,
            token=user_token.verification_uuid,
        )
    except OperationalError:
        logger.info('Check redis connection, email will be sent in sync mode')
        raise Http404
