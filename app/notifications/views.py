import logging
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, DeleteView
from notifications.models import Notification, NotificationInstance

logger = logging.getLogger(__name__)


class BaseNotificationDetailView(DetailView):
    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        profile_id = request.user.profile.pk
        notification_id = kwargs['pk']
        try:
            notification_instance = NotificationInstance.objects.get(
                Q(notification_id=notification_id) & Q(profile_id=profile_id)
            )
            self.kwargs['notification_instance'] = notification_instance
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

        return super(BaseNotificationDetailView, self).dispatch(request, *args, **kwargs)


class NotificationsListView(ListView):
    model = Notification
    template_name = 'notifications/notifications-box.html'
    context_object_name = 'notifications_instances'
    paginate_by = 9

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = NotificationInstance.objects.select_related(
            'notification').filter(profile=self.request.user.profile).order_by('-notification__created_at')
        if self.request.GET.get('new', '').lower() == 'true':
            qs = qs.filter(is_read=False)
        context['notifications_instances'] = qs
        return context


class NotificationDetailView(BaseNotificationDetailView):
    template_name = 'notifications/notification-detail.html'
    model = Notification
    context_object_name = 'notification'
    success_url = reverse_lazy('notifications')

    def get(self, request, *args, **kwargs):
        self.kwargs['notification_instance'].is_read = True
        self.kwargs['notification_instance'].save()
        return super().get(request, *args, **kwargs)


class NotificationDeleteView(BaseNotificationDetailView, DeleteView):
    model = Notification
    success_url = reverse_lazy('notifications')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.kwargs['notification_instance'].delete()
        return HttpResponseRedirect(success_url)
