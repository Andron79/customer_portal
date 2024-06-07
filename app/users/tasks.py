from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model

from django.core.mail import send_mail, EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from customer_portal import settings

logger = get_task_logger(__name__)


@shared_task()
def send_verification_email(
        user_id: int = None,
        token: str = None,
        template='email/email_confirmation.html'
):
    user = None
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=user_id)
    except UserModel.DoesNotExist:
        logger.error(f"Попытка отправить подтверждение email несуществующему пользователю {user_id}")

    context = {
        'user': user,
        'token': urlsafe_base64_encode(force_bytes(token)),
        'domain': settings.DOMAIN,
    }
    msg_html = render_to_string(template, context=context)
    send_mail(
        subject='Активация аккаунта на портале Customer Portal',
        message='',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
        html_message=msg_html
    )
    logger.info(f"Подтверждение активации аккаунта отправлено пользователю {user.profile.name} на почту {user.email}")


@shared_task()
def send_notification_emails(
        subject: str = None,
        message: str = None,
        recipient_list: list = None,
        template='email/email_notification.html'
):
    context = {
        'domain': settings.DOMAIN,
        'subject': subject,
        'message': message
    }
    msg_html = render_to_string(template, context=context)

    emails = []
    for recipient in recipient_list:
        email = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, [recipient])
        email.attach_alternative(msg_html, 'text/html')
        emails.append(email)
    return get_connection().send_messages(emails)
