import logging

from django.db import transaction
from django.db.models import signals
from django.dispatch import receiver

from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType

from customer_portal import settings
from users.models import UserProfile, generate_token_and_send_verification_email, CustomUser

logger = logging.getLogger(__name__)


@receiver(signals.post_delete, sender=UserProfile)
def delete_user(sender, instance: UserProfile = None, **kwargs):
    try:
        instance.user
    except CustomUser.DoesNotExist:
        pass
    else:
        instance.user.delete()


@receiver(signals.post_save, sender=UserProfile)
@transaction.atomic
def send_activation_mail_after_create_profile(sender, instance: UserProfile, created: bool, **kwargs):
    if not created:
        return

    user_profile = UserProfile.objects.get(user=instance.user)
    logger.info(
        f'Профиль пользователя {user_profile.user.email}, '
        f'id={user_profile.user.pk} создан!'
    )
    if not user_profile.user.is_active:
        generate_token_and_send_verification_email(user_id=user_profile.user.pk)
        LogEntry.objects.log_action(
            user_id=user_profile.user.pk,
            content_type_id=ContentType.objects.get_for_model(CustomUser).pk,
            object_id=user_profile.user.id,
            object_repr=f'{settings.DEFAULT_FROM_EMAIL}: '
                        f'Токен на активацию аккаунта {user_profile.name} '
                        f'отправлен на почту {user_profile.user.email}',
            action_flag=ADDITION
        )
