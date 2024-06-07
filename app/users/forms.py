import logging
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, UserProfile

logger = logging.getLogger(__name__)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class CreateUserForm(forms.ModelForm):
    COMPANY_ADMIN = 1
    COMPANY_EMPLOYEE = 2

    ROLE_CHOICES = (
        (COMPANY_ADMIN, _('Company Admin')),
        (COMPANY_EMPLOYEE, _('Company Employee')),
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        label=_("Role"),
        widget=forms.Select,
        required=True
    )
    name = forms.CharField(
        max_length=100,
        required=True,
        label=_("Name"),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _("Retype Password"),
                'autocomplete': 'false',
                'class': 'type="password" name="password"',
            }
        ),
        label=_("Confirm Password")
    )

    class Meta:
        model = CustomUser
        fields = ('name', 'email', 'password', 'password2', 'role', 'is_active')

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {
                'placeholder': _("Name"),
                'autocomplete': 'false',
            },

        ),
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': _("Email"),
                'class': 'type="email" name="email"',
                'autocomplete': 'false'
            }
        ),
        self.fields['password'].widget.attrs.update(
            {
                'placeholder': _("Password"),
                'autocomplete': 'false',
                'class': 'type="password" name="password"',
            }
        ),

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            password_validation.validate_password(password, self.instance)
        except forms.ValidationError as error:
            self.add_error('password', error)
        return password

    def clean(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            self.add_error('password', _("Password not match!"))
            self.add_error('password2', _("Password not match!"))
        if (email := cd.get('email')) and CustomUser.objects.filter(email=email).exists():
            self.add_error('email', _("User with this email exists!"))
        return cd


class UpdateUserForm(forms.ModelForm):
    COMPANY_ADMIN = 1
    COMPANY_EMPLOYEE = 2

    ROLE_CHOICES = (
        (COMPANY_ADMIN, _('Company Admin')),
        (COMPANY_EMPLOYEE, _('Company Employee')),
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select,
        label=_("Role"),
    )
    name = forms.CharField(
        max_length=100,
        required=True,
        label=_("Name")
    )

    class Meta:
        model = UserProfile
        fields = ('name', 'role',)
