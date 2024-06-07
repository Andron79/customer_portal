import logging

from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView

from pages.models import (
    Information,
    Document,
    FAQ,
    File,
    Tutorial
)
from pages.yandex_s3_storage import PrivateDownload

logger = logging.getLogger(__name__)


class UserContentListView(ListView):
    def get_queryset(self):
        if self.request.user.pk:
            try:
                return self.model.objects.filter(
                    company=self.request.user.profile.company).union(
                    self.model.objects.filter(
                        product__company_types=self.request.user.profile.company.company_type)
                )
            except ObjectDoesNotExist:
                return self.model.objects.filter(is_public=True)
        else:
            return self.model.objects.filter(is_public=True)


class InformationView(UserContentListView):
    model = Information
    template_name = 'pages/information.html'
    context_object_name = 'informations'


class FileView(UserContentListView):
    model = File
    template_name = 'pages/files.html'
    context_object_name = 'files'


class DocumentationView(UserContentListView):
    model = Document
    template_name = 'pages/documentation.html'
    context_object_name = 'documents'


# @cache_control(private=True)
class TutorialView(UserContentListView):
    model = Tutorial
    template_name = 'pages/tutorial.html'
    context_object_name = 'tutorials'


class FaqView(UserContentListView):
    model = FAQ
    template_name = 'pages/FAQ.html'
    context_object_name = 'FAQs'


class PrivateDocumentDownload(PrivateDownload):
    model = Document


class PrivateFileDownload(PrivateDownload):
    model = File
