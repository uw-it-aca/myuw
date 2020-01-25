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
log_format = "Deleted django sessions expired before {}, Time={} seconds"


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('total_days', type=int,
                            help="param1: total_days")
        # total_days: the total number of days back where
        #             the earliest expired sessions exist

    def handle(self, *args, **options):
        total_days = options['total_days']
        now = timezone.now()
        for ddelta in range(total_days, 0, -1):
            cut_off_dt = now - timedelta(days=ddelta)

            day_session_count = Session.objects.filter(
                expire_date__lt=cut_off_dt).count()
            if day_session_count > 10000:
                start_hr, inc_hrs = get_cut_off_params(day_session_count)
                for hdelta in range(start_hr, 0, inc_hrs):
                    dthour = cut_off_dt - timedelta(hours=hdelta)
                    run_delete(dthour)

            run_delete(cut_off_dt)


def get_cut_off_params(day_session_count):
    if day_session_count <= 50000:
        # further split into 6 sets
        return 20, -4
    if day_session_count <= 100000:
        # further split into 12 sets
        return 22, -2
    # further split into 24 sets
    return 23, -1


def run_delete(cut_off_dt):
    qset = Session.objects.filter(expire_date__lt=cut_off_dt)
    if qset.exists():
        timer = Timer()
        qset.delete()
        logger.info(log_format.format(
            cut_off_dt.strftime("%Y-%m-%d %H:%M:%S"),
            timer.get_elapsed()))
        time.sleep(3)
