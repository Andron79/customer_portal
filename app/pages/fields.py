from django.core.exceptions import ValidationError
from django.core.files import File
from django.db import models

from customer_portal import settings
from pages.utils import convert_file_size_to_str
from pages.yandex_s3_storage import PrivateClientUserContentStorage


def validate_file_size(_file: File, limit: int = settings.FILE_UPLOAD_SIZE_LIMIT):
    if limit <= 0:
        return
    if _file.size > limit:
        raise ValidationError(f'File too large. Size should not exceed {convert_file_size_to_str(limit)}.')


class LimitedSizeFileField(models.FileField):
    def __init__(self, verbose_name=None, name=None, upload_to="", storage=None, **kwargs):
        if validate_file_size not in (validators := kwargs.pop('validators', [])):
            validators.append(validate_file_size)
        super().__init__(verbose_name=verbose_name, name=name, upload_to=upload_to, storage=storage,
                         validators=validators, **kwargs)


class PrivateFileField(LimitedSizeFileField):
    def __init__(self, verbose_name=None, name=None, upload_to='', storage=None, **kwargs):
        if not (storage or settings.AWS_PRIVATE_MEDIA_LOCATION):
            raise ValidationError("Set AWS_PRIVATE_MEDIA_LOCATION settings key in order to user PrivateFileField")
        super().__init__(verbose_name, name, upload_to, storage=PrivateClientUserContentStorage(), **kwargs)
