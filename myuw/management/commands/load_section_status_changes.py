import logging
from django.core.management.base import BaseCommand, CommandError
from myuw.event.section_status import SectionStatusProcessor
from myuw.logger.timer import Timer
from aws_message.gather import Gather


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Loads Section Status change events from SQS"

    def handle(self, *args, **options):
        timer = Timer()
        try:
            Gather(processor=SectionStatusProcessor()).gather_events()
            logger.info("Total Time: %f seconds",  timer.get_elapsed())
        except Exception as err:
            raise CommandError("Cause: %s" % err)
