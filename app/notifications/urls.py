from django.urls import path

from notifications.views import (
    NotificationsListView,
    NotificationDeleteView,
    NotificationDetailView,
)

urlpatterns = [
    path('notifications/', NotificationsListView.as_view(), name='notifications'),
    path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification'),
    path('notifications/<int:pk>/delete/', NotificationDeleteView.as_view(), name='delete-notification')
]
