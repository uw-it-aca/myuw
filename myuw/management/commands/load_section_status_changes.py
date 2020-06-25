"""
Loads Section Status change events from SQS
"""

import logging
import traceback
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from myuw.event.section_status import SectionStatusProcessor
from myuw.logger.timer import Timer
from myuw.util.settings import get_cronjob_recipient, get_cronjob_sender
from aws_message.gather import Gather

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        logger.info("Start ...")

        timer = Timer()
        try:
            Gather(processor=SectionStatusProcessor()).gather_events()
            logger.info("Total Time: {} seconds".format(timer.get_elapsed()))
        except Exception as ex:
            logger.error(ex)
            send_mail("Loads Section Status change Cron",
                      "{}".format(traceback.format_exc(chain=False)),
                      "{}@uw.edu".format(get_cronjob_sender()),
                      ["{}@uw.edu".format(get_cronjob_recipient())])
        logger.info("End ...")
