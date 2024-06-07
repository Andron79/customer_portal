from django.core.management import BaseCommand

from customer_portal.settings import AWS_CLIENT, AWS_PRIVATE_MEDIA_LOCATION, AWS_STORAGE_BUCKET_NAME
from pages.models import File, Document
from pages.utils import get_remote_file_size, logger as utils_logger, suppress_logger


class Command(BaseCommand):
    help = 'Clean up lost remote files in databases'

    def handle(self, *args, **kwargs):
        with suppress_logger(utils_logger):
            for model in (File, Document):
                for model_obj in model.objects.all():
                    size = get_remote_file_size(
                        client=AWS_CLIENT,
                        bucket=AWS_STORAGE_BUCKET_NAME,
                        key=f'{AWS_PRIVATE_MEDIA_LOCATION}/{str(model_obj.file)}'
                    )
                    if not size:
                        model_obj.delete()
                        self.stdout.write(self.style.WARNING(
                            f"The {model_obj} object is missing in the file storage, deletion from the database")
                        )

        self.stdout.write(self.style.SUCCESS("Database cleaned!"))
