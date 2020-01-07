"""
The django clearsessions commend internally calls:
   cls.get_model_class().objects.filter(
       expire_date__lt=timezone.now()).delete()
which could lock the DB table for a long time when
 having a large number of records to delete.

To prevent the job running forever, we only delete 40000
expired django sessions in a single run
"""

import logging
from django.core.management.base import BaseCommand, CommandError
from django.contrib.sessions.models import Session
from django.utils import timezone

logger = logging.getLogger(__name__)
DEL_SIZE = 40000


class Command(BaseCommand):

    def handle(self, *args, **options):
        i = 0
        for record in Session.objects.filter(expire_date__lt=timezone.now()):
            i += 1
            if i <= DEL_SIZE:
                try:
                    record.delete()
                except Exception as ex:
                    logger.error("{} {}".format(record, str(ex)))
