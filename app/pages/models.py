import logging

from django.db import models
from django.dispatch import receiver
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField
from customer_portal.settings import (
    AWS_CLIENT,
    AWS_STORAGE_BUCKET_NAME,
    PRIVATE_URL_EXPIRES_IN_SECONDS
)
from pages.fields import PrivateFileField
from pages.utils import (
    convert_file_size_to_str,
    convert_file_name_to_str,
    convert_file_format_to_str
)
from customer_dashboard.models import (
    BaseModel,
    Company,
    CompanyType
)

logger = logging.getLogger(__name__)


class Product(BaseModel):
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=250,
        unique=True,
        blank=False,
        null=False
    )
    company_types = models.ManyToManyField(
        CompanyType,
        verbose_name=_('Company types'),
        blank=True
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _("Products")


class PageBaseModel(models.Model):
    created_at = models.DateField(
        verbose_name=_('Created at'),
        auto_now_add=True
    )
    updated_at = models.DateField(
        verbose_name=_('Updated at'),
        auto_now=True)
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=250,
        unique=True,
        blank=False,
        null=False
    )
    description = models.TextField(
        verbose_name=_('Description'),
        max_length=2500,
        blank=True,
        null=True
    )
    is_public = models.BooleanField(
        verbose_name=_('Display in Public Page'),
        default=False
    )

    class Meta:
        abstract = True


class Information(PageBaseModel):
    description = RichTextUploadingField(
        verbose_name=_('Description'),
        blank=True,
        null=True
    )
    company = models.ManyToManyField(
        Company,
        verbose_name=_('Companies'),
        blank=True
    )
    product = models.ManyToManyField(
        Product,
        verbose_name=_('Products'),
        blank=True
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = _('Information')
        verbose_name_plural = _("Information's")


class Document(PageBaseModel):
    file = PrivateFileField(
        verbose_name=_('File'),
        upload_to='Documents',
        blank=False,
        null=False,
    )
    company = models.ManyToManyField(
        Company,
        verbose_name=_('Companies'),
        blank=True
    )
    product = models.ManyToManyField(
        Product,
        verbose_name=_('Products'),
        blank=True
    )
    file_size = models.PositiveBigIntegerField(
        verbose_name=_('File size'),
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.title)

    @property
    def file_format(self):
        return convert_file_format_to_str(self.file)

    file_format.fget.short_description = _('File format')

    @property
    def file_name(self):
        return convert_file_name_to_str(self.file)

    file_name.fget.short_description = _('File name')

    @property
    def humanized_file_size(self):
        return convert_file_size_to_str(self.file_size)

    humanized_file_size.fget.short_description = _('File size')

    @property
    def storage_key(self):
        return f"{self.file.storage.location}/{self.file.name}"

    def get_expiring_url(self, expires_in: int = PRIVATE_URL_EXPIRES_IN_SECONDS):
        """
        Generates a permissioned url that will expire at `expires_in` seconds.
        Defaults to 30 minutes.
        """
        if self.file is not None:
            url = AWS_CLIENT.generate_presigned_url(
                ClientMethod="get_object",
                Params={
                    "Bucket": AWS_STORAGE_BUCKET_NAME,
                    "Key": self.storage_key,
                },
                ExpiresIn=expires_in,
            )
            return url

        raise Http404

    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')

    def save(self, *args, **kwargs):
        if not self.file_size:
            self.file_size = self.file.size
        super().save(*args, **kwargs)


class File(PageBaseModel):
    file = PrivateFileField(
        verbose_name=_('File'),
        upload_to='Files',
        blank=False,
        null=False
    )
    company = models.ManyToManyField(
        Company,
        verbose_name=_('Companies'),
        blank=True
    )
    product = models.ManyToManyField(
        Product,
        verbose_name=_('Products'),
        blank=True,
    )

    file_size = models.PositiveBigIntegerField(
        verbose_name=_('File size'),
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.title)

    @property
    def file_name(self):
        return convert_file_name_to_str(self.file)

    file_name.fget.short_description = _('File name')

    @property
    def file_format(self):
        return convert_file_format_to_str(self.file)

    file_format.fget.short_description = _('File format')

    @property
    def humanized_file_size(self):
        return convert_file_size_to_str(self.file_size)

    humanized_file_size.fget.short_description = _('File size')

    @property
    def storage_key(self):
        return f"{self.file.storage.location}/{self.file.name}"

    def get_expiring_url(self, expires_in: int = PRIVATE_URL_EXPIRES_IN_SECONDS):
        """
        Generates a permissioned url that will expire at `expires_in` seconds.
        Defaults to 30 minutes.
        """
        if self.file is not None:
            url = AWS_CLIENT.generate_presigned_url(
                ClientMethod="get_object",
                Params={
                    "Bucket": AWS_STORAGE_BUCKET_NAME,
                    "Key": self.storage_key,
                },
                ExpiresIn=expires_in,
            )
            return url

        raise Http404

    class Meta:
        verbose_name = _('File')
        verbose_name_plural = _('Files')

    def save(self, *args, **kwargs):
        if not self.file_size:
            self.file_size = self.file.size
        super().save(*args, **kwargs)


class Tutorial(PageBaseModel):
    image = models.ImageField(
        upload_to="images/",
        null=False,
        blank=False,
        verbose_name=_('Cover')
    )
    external_url = models.URLField(
        verbose_name=_('External URL'),
        null=False,
        blank=False
    )
    company = models.ManyToManyField(
        Company,
        verbose_name=_('Companies'),
        blank=True
    )
    product = models.ManyToManyField(
        Product,
        verbose_name=_('Products'),
        blank=True,
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = _('Tutorial')
        verbose_name_plural = _("Tutorials")


class FAQ(BaseModel):
    question = models.CharField(
        max_length=500,
        verbose_name=_('Question')
    )
    answer = RichTextUploadingField(
        verbose_name=_('Answer'),
        blank=True,
        null=True
    )
    company = models.ManyToManyField(
        Company,
        verbose_name=_('Companies'),
        blank=True
    )
    product = models.ManyToManyField(
        Product,
        verbose_name=_('Products'),
        blank=True,
    )
    is_public = models.BooleanField(
        verbose_name=_('Display in Public Page'),
        default=False
    )

    def __str__(self):
        return str(self.question)

    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _("FAQs")


@receiver(models.signals.post_delete, sender=File)
def s3_auto_delete_file_on_delete_from_admin(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(save=False)


@receiver(models.signals.post_delete, sender=Document)
def s3_auto_delete_document_on_delete_from_admin(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(save=False)
