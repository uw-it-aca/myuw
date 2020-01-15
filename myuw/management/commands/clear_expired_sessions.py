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
from datetime import timedelta
import time
from django.core.management.base import BaseCommand, CommandError
from django.contrib.sessions.models import Session
from django.utils import timezone
from myuw.logger.timer import Timer

logger = logging.getLogger(__name__)
begin_delta = 1920
log_format = "Deleted django sessions expired before {}, Time={} seconds"


class Command(BaseCommand):

    def handle(self, *args, **options):
        now = timezone.now()
        for ddelta in range(begin_delta, 0, -1):
            timer = Timer()
            cut_off_dt = now - timedelta(days=ddelta)
            qset = Session.objects.filter(expire_date__lt=cut_off_dt)
            if qset.exists():
                qset.delete()
                logger.info(log_format.format(cut_off_dt.date(),
                                              timer.get_elapsed()))
                time.sleep(5)
