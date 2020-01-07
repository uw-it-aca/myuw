"""
The django clearsessions commend internally calls:
   cls.get_model_class().objects.filter(
       expire_date__lt=timezone.now()).delete()
which could lock the DB table for a long time when
having a large number of records to delete.

To prevent the job running forever, we only delete a limit number of
expired django sessions in a single run
"""

import logging
from django.core.management.base import BaseCommand, CommandError
from django.contrib.sessions.models import Session
from django.utils import timezone
from myuw.logger.timer import Timer

logger = logging.getLogger(__name__)
DEL_SIZE = 10000


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            timer = Timer()
            qs = Session.objects.filter(
                expire_date__lt=timezone.now())[0:DEL_SIZE]
            if qs.exists():
                qs.delete()
            logger.info(
                "clear_expired_sessions, Time={} seconds".format(
                    timer.get_elapsed()))
        except Exception as ex:
            logger.error(str(ex))
