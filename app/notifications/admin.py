import logging
from django.contrib import admin
from django.db import transaction
from notifications.models import Notification, NotificationInstance
from pages.admin import UserContentModelAdmin
from users.models import UserProfile
from users.tasks import send_notification_emails
from django.db.models import Q

logger = logging.getLogger(__name__)


class NotificationAdmin(UserContentModelAdmin):
    model = Notification
    list_display = ('created_at', 'to_email', 'subject', 'companies_list', 'company_types_list',)
    list_filter = ('company', 'company_types')
    date_hierarchy = 'created_at'
    search_fields = ('subject',)
    empty_value_display = '🚫️'
    filter_horizontal = ('company_types', 'company',)
    readonly_fields = ('created_at',)
    fields = ('subject', 'created_at', 'to_email', 'text', 'company', 'company_types',)
    list_display_links = ('created_at', 'subject',)
    save_as = False
    save_on_top = True
    save_as_continue = False
    change_readonly_fields = (
        'subject',
        'created_at',
        'to_email',
        'text',
        'company',
        'company_types',
        'companies_list',
        'company_types_list'
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        notification_profiles_qs = UserProfile.objects.filter(
            Q(company_id__in=request.POST.getlist('company'))
            | Q(company__company_type__in=request.POST.getlist('company_types'))
        )

        with transaction.atomic():
            recipient_list = [profile.user.email for profile in notification_profiles_qs]
            NotificationInstance.objects.bulk_create(
                [
                    NotificationInstance(
                        is_read=False,
                        notification_id=obj.pk,
                        profile_id=profile.pk
                    )
                    for profile in notification_profiles_qs
                ]
            )
            if obj.to_email:

                send_notification_emails(
                    subject=obj.subject,
                    message=obj.text,
                    recipient_list=recipient_list
                )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(NotificationAdmin, self).get_readonly_fields(request, obj)
        if obj:
            return self.change_readonly_fields
        return readonly_fields


admin.site.register(Notification, NotificationAdmin)
