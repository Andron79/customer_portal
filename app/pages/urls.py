from django.urls import path
from pages.views import (
    FaqView,
    InformationView,
    DocumentationView,
    FileView,
    TutorialView,
    PrivateDocumentDownload,
    PrivateFileDownload
)

from users.views import (
    UsersProfileListView,
    UserUpdateView,
    UserCreateView,
    UserDeleteView,
    ProfileUpdateView,
    ConfirmedUserView,
    ActivateAccountView,
    SendEmailVerificationTokenView
)

urlpatterns = [
    path('information/', InformationView.as_view(), name='information'),
    path('files/', FileView.as_view(), name='files'),
    path('documentations/', DocumentationView.as_view(), name='documentations'),
    path('tutorials/', TutorialView.as_view(), name='tutorials'),
    path('faq/', FaqView.as_view(), name='faq'),
    path('users/', UsersProfileListView.as_view(), name='users'),
    path('users/sent-message/', ConfirmedUserView.as_view(), name='sent-message'),
    path('users/send-email-verification-token/',
         SendEmailVerificationTokenView.as_view(), name='send-email-verification-token'),
    path('users/activate-account/<uidb64>/', ActivateAccountView.as_view(), name='activate-account'),
    path('users/create-user/', UserCreateView.as_view(), name='create-user'),
    path('users/update-profile/', ProfileUpdateView.as_view(), name='update-profile'),
    path('users/update-user/<int:pk>', UserUpdateView.as_view(), name='update-user'),
    path('users/delete-user/<int:pk>', UserDeleteView.as_view(), name='delete-user'),
    path('download-documet/<int:pk>', PrivateDocumentDownload.as_view(), name='download-document'),
    path('download-file/<int:pk>', PrivateFileDownload.as_view(), name='download-file'),
]
