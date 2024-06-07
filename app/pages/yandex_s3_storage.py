import logging
from abc import ABC

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView
from storages.backends.s3boto3 import S3Boto3Storage

from customer_portal.settings import (
    AWS_PRIVATE_MEDIA_LOCATION,
    AWS_PUBLIC_MEDIA_LOCATION,
    AWS_DEFAULT_ACL, AWS_CLIENT, AWS_STORAGE_BUCKET_NAME
)
from pages.utils import get_remote_file_size

logger = logging.getLogger(__name__)


class ClientUserContentStorage(S3Boto3Storage, ABC):
    location = AWS_PUBLIC_MEDIA_LOCATION
    file_overwrite = False


class PrivateClientUserContentStorage(S3Boto3Storage, ABC):
    location = AWS_PRIVATE_MEDIA_LOCATION
    default_acl = AWS_DEFAULT_ACL
    file_overwrite = False
    custom_domain = False


class PrivateDownload(RedirectView):
    model = None

    def get_redirect_url(self, *args, **kwargs):
        """
        Override this method so the view doesn't try to do any
        string interpolation.
        """
        return self.url

    def get(self, request, *args, **kwargs):
        content_obj = get_object_or_404(self.model, pk=kwargs["pk"])
        size = get_remote_file_size(
            client=AWS_CLIENT,
            bucket=AWS_STORAGE_BUCKET_NAME,
            key=f'{AWS_PRIVATE_MEDIA_LOCATION}/{str(content_obj.file)}'
        )
        if not size:
            raise Http404

        if request.user.pk:
            content_list = self.model.objects.filter(
                company=self.request.user.profile.company).union(
                self.model.objects.filter(
                    product__company_types=self.request.user.profile.company.company_type)
            )
            if content_list and content_obj in content_list:
                self.url = content_obj.get_expiring_url()
                return super().get(request, *args, **kwargs)
            else:
                raise Http404

        elif content_obj.is_public:
            self.url = content_obj.get_expiring_url()
            return super().get(request, *args, **kwargs)

        else:
            raise Http404
