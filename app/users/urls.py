from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    LogoutView,
    PasswordChangeView,
    LoginView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView
)

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(template_name='registration/login-v2.html'), name='login'),

    path('change-password/', PasswordChangeView.as_view(success_url=reverse_lazy('password_change_done')),
         name='change_password'),
    path('change-password/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('passwort-reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
