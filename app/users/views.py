import logging
import uuid
from django.contrib import messages
from django.contrib.admin.models import LogEntry, DELETION, ADDITION, CHANGE

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
    TemplateView,
)

from users.forms import (
    CreateUserForm,
    UpdateUserForm,
)
from users.models import (
    UserProfile,
    CustomUser,
    EmailVerificationToken,
    generate_token_and_send_verification_email
)

logger = logging.getLogger(__name__)


class AdminRequiredMixin(LoginRequiredMixin):

    def __init__(self):
        self.kwargs = None
        self.request = None

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_active and self.request.user.profile.company:
            if self.request.user.profile.role != UserProfile.COMPANY_ADMIN:
                raise Http404
        else:
            raise Http404
        return super(AdminRequiredMixin, self).dispatch(request, *args, **kwargs)


class UsersProfileListView(AdminRequiredMixin, ListView):
    model = UserProfile
    template_name = 'users/users_list.html'
    context_object_name = 'users_profiles'

    def get_queryset(self):
        return UserProfile.objects.select_related('user').filter(
            company__userprofile__user_id=self.request.user.pk
        ).exclude(user__is_superuser=True)


class UserCreateView(AdminRequiredMixin, CreateView):
    model = CustomUser
    form_class = CreateUserForm
    success_url = reverse_lazy('sent-message')
    template_name = 'users/user_create.html'
    extra_context = {}

    def get(self, request, *args, **kwargs):
        max_users = self.request.user.profile.company.max_num_company_users
        self.extra_context.update(
            users_count=UserProfile.objects.filter(company=self.request.user.profile.company).distinct().count())
        self.extra_context.update(users_remaining_limit=max_users - self.extra_context['users_count'])
        if self.extra_context['users_remaining_limit'] <= 0:
            messages.add_message(
                self.request,
                messages.ERROR,
                _("You have reached the limit for user registration. "
                  "Delete any user or contact Getmobit technical support to increase the limit.")
            )
            return HttpResponseRedirect(reverse_lazy('sent-message'))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form, **kwargs):
        response = super(UserCreateView, self).form_valid(form)
        user = form.save(commit=False)
        password = form.cleaned_data['password']
        user.set_password(password)
        name = form.cleaned_data['name']
        role = form.cleaned_data['role']
        company = self.request.user.profile.company
        user.save()

        LogEntry.objects.log_action(
            user_id=self.request.user.pk,
            content_type_id=ContentType.objects.get_for_model(CustomUser).pk,
            object_id=user.id,
            object_repr=f'Пользователь {user.email} создан.',
            action_flag=ADDITION
        )
        UserProfile.objects.create(user=user, name=name, role=role, company=company)
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _("A link to activate the account was sent to this email: ")
        )
        messages.add_message(self.request, messages.SUCCESS, user.email)

        return response


class UserUpdateView(AdminRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UpdateUserForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('users')

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        profile_id = int(self.kwargs['pk'])
        self.profile = get_object_or_404(UserProfile, pk=profile_id)
        if self.profile.company.pk != self.request.user.profile.company.pk:
            raise Http404

        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        LogEntry.objects.log_action(
            user_id=self.request.user.pk,
            content_type_id=ContentType.objects.get_for_model(CustomUser).pk,
            object_id=self.request.user.profile.pk,
            object_repr=f'Пользователь {self.profile.user.email} изменен!',
            action_flag=CHANGE
        )
        return super().form_valid(form)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    fields = ('name',)
    template_name = 'users/user_update_profile.html'
    success_url = reverse_lazy('information')

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.request.user.profile.pk)

    def form_valid(self, form):
        self.object = form.save()
        LogEntry.objects.log_action(
            user_id=self.request.user.pk,
            content_type_id=ContentType.objects.get_for_model(CustomUser).pk,
            object_id=int(self.request.user.profile.pk),
            object_repr=f'Пользователь {self.request.user.email} изменил собственный профиль!',
            action_flag=CHANGE
        )
        return super().form_valid(form)


class UserDeleteView(AdminRequiredMixin, DeleteView):
    model = UserProfile
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('users')

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        profile_id = int(self.kwargs['pk'])
        self.profile = get_object_or_404(UserProfile, pk=profile_id)
        if self.profile.company.pk != self.request.user.profile.company.pk:
            raise Http404

        return super(UserDeleteView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        LogEntry.objects.log_action(
            user_id=self.request.user.pk,
            content_type_id=ContentType.objects.get_for_model(CustomUser).pk,
            object_id=int(self.kwargs['pk']),
            object_repr=f'Пользователь {self.profile.user.email} удален!',
            action_flag=DELETION
        )
        return super().form_valid(form)


class ConfirmedUserView(TemplateView):
    model = CustomUser
    template_name = 'message_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context.get('messages', None):
            return HttpResponseRedirect(reverse_lazy('users'))
        return context


class SendEmailVerificationTokenView(AdminRequiredMixin, CreateView):
    model = EmailVerificationToken
    success_url = reverse_lazy('sent-message')

    @method_decorator(login_required())
    def post(self, request, *args, **kwargs):
        profile_id = int(self.request.POST.get('profile_id'))
        profile = UserProfile.objects.get(pk=profile_id)
        if self.request.user.profile.company != profile.company:
            raise Http404

        if profile.user.is_active:
            return HttpResponseRedirect(self.success_url)

        generate_token_and_send_verification_email(user_id=profile.user.pk)
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _("A link to activate the account was sent to this email: ")
        )
        messages.add_message(self.request, messages.SUCCESS, profile.user.email)
        return HttpResponseRedirect(self.success_url)


class ActivateAccountView(TemplateView):
    template_name = "message_page.html"

    @transaction.atomic
    def dispatch(self, *args, **kwargs):
        try:
            token = uuid.UUID(urlsafe_base64_decode(self.kwargs['uidb64']).decode("utf-8")).hex
        except ValueError:
            messages.add_message(self.request, messages.ERROR, _('Bad activation token'))
            return super().dispatch(*args, **kwargs)

        try:
            user = CustomUser.objects.get(email_verification_token__verification_uuid=token)
        except ObjectDoesNotExist:
            messages.add_message(self.request, messages.ERROR, _('Token is not valid'))
            return super().dispatch(*args, **kwargs)

        CustomUser.objects.filter(pk=user.pk).update(is_active=True)
        EmailVerificationToken.objects.filter(user_id=user.pk).update(verification_uuid=None)
        messages.add_message(self.request, messages.SUCCESS,
                             _("The email address has been successfully confirmed!"))
        return super().dispatch(*args, **kwargs)
