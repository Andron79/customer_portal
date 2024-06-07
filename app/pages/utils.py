from contextlib import contextmanager
from pathlib import Path
from typing import Union, Optional

from botocore.exceptions import ClientError
from django.core.files import File
import logging


logger = logging.getLogger(__name__)


@contextmanager
def suppress_logger(_logger: Union[logging.Logger, str]):
    if not _logger:
        raise ValueError("Either logger name or instance should be specified")
    if isinstance(_logger, str):
        _logger = logging.getLogger(_logger)

    _was_disabled = _logger.disabled
    _logger.disabled = True
    yield
    _logger.disabled = _was_disabled


def get_remote_file_size(client, bucket: str, key: str) -> Union[int, None]:
    """return the object size if exists, else None"""
    try:
        obj = client.head_object(Bucket=bucket, Key=key)
        return obj.get('ContentLength')
    except ClientError as exc:
        if exc.response['Error']['Code'] == '404':
            logger.warning(f'Object by path {key} not exist in storage')
        else:
            logger.exception(f"Error while trying to access object by path {key}")
        return None


def convert_file_name_to_str(file: Optional[File] = None) -> str:
    return Path(file.name).name if file else ""


def convert_file_format_to_str(file: Optional[File] = None) -> str:
    return Path(file.name).suffix[1:].upper() if file else ""


def convert_file_size_to_str(file_size: Optional[int] = None) -> str:
    if not file_size:
        return "0 b"

    space_modifiers = " kMGT"
    idx = 0
    while abs(file_size) >= 1000:
        file_size /= 1000
        idx += 1
    return f"{round(file_size, 2)}" \
           f"{space_modifiers[idx] if idx < len(space_modifiers) else '?'}" \
           f"b"
