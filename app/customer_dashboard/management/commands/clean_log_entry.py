from django.contrib.admin.models import LogEntry
from django.core.management import BaseCommand
from pages.utils import logger as utils_logger, suppress_logger


class Command(BaseCommand):
    help = 'Clean LogEntries'

    def handle(self, *args, **kwargs):
        with suppress_logger(utils_logger):
            deleted_entries = LogEntry.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Log Entry cleaned!. {deleted_entries[0]} entries removed."))
