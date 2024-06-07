from django import template
from notifications.models import NotificationInstance

register = template.Library()


@register.simple_tag
def notification_count(user):
    return NotificationInstance.objects.filter(
        profile_id=user.profile
    ).count()
