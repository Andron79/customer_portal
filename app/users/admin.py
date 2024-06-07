import logging

from django.contrib.auth.models import Group

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin

from django.utils.translation import gettext_lazy as _

from pages.admin import UserContentModelAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, UserProfile

from django.contrib.admin.models import LogEntry

logger = logging.getLogger(__name__)


class UserProfileInline(admin.TabularInline):
    model = UserProfile
    extra = 1
    max_num = 1
    min_num = 1
    can_delete = False
    verbose_name_plural = _('Profile')
    view_on_site = False


class CustomUserAdmin(UserContentModelAdmin, UserAdmin):
    inlines = [UserProfileInline, ]
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    verbose_name_plural = 'Profiles'
    list_display_links = ('email',)
    list_display = (
        'email',
        'profile_company',
        'profile_name',
        'profile_role',
        'date_joined',
        'is_superuser',
        'is_staff',
        'is_active',
    )
    list_filter = ('profile__company__title', 'is_superuser', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'date_joined',)}),
        (_('Permissions'), {'fields': ('is_superuser', 'is_staff', 'is_active', 'groups',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_superuser', 'is_staff', 'is_active',)}
         ),
    )
    search_fields = ('email', 'profile__company__title')
    ordering = ('profile__company__title',)
    filter_horizontal = ('groups', 'user_permissions',)
    save_as_continue = False
    save_as = False

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True
            form.base_fields['is_staff'].disabled = True
        form.base_fields['is_active'].disabled = True
        return form

    @admin.display(description=_('Name'))
    def profile_name(self, obj):
        return obj.profile.name

    @admin.display(description=_('Company'), ordering='profile__company__title')
    def profile_company(self, obj):
        return obj.profile.company

    def profile_role(self, obj):
        return obj.profile.get_role_display()

    profile_role.short_description = _('Role')


class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ('name',)


class GroupsAdmin(GroupAdmin):
    list_display = GroupAdmin.list_display + ('user_count_in_group',)

    def user_count_in_group(self, obj):
        return obj.user_set.count()

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'
    list_filter = [
        'user',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [

        'action_time',
        'user',
        # 'profile_name',
        'company_name',
        'content_type',
        'action_flag',
        'object_repr'
    ]

    @admin.display(description=_('Name'))
    def profile_name(self, obj):
        return UserProfile.objects.get(user_id=obj.user_id).name

    # @admin.display(description=_('Name'))
    # def object(self, obj):
    #     return obj.__str__()

    @admin.display(description=_('Company'))
    def company_name(self, obj):
        return UserProfile.objects.get(user_id=obj.user_id).company.title

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True


admin.site.unregister(Group)
admin.site.register(Group, GroupsAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
