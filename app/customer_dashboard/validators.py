from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


def validate_digit(value):
    if not all(map(str.isdigit, value)):
        raise ValidationError(
            _('Only digit characters (0-9)')
        )
