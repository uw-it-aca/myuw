from django.core.management.base import BaseCommand, CommandError
from myuw.event. section_status import SectionStatusProcessor
from aws_message.gather import Gather, GatherException


class Command(BaseCommand):
    help = "Loads Person change events from SQS"

    def handle(self, *args, **options):
        try:
            Gather(processor=SectionStatusProcessor()).gather_events()
        except GatherException as err:
            raise CommandError(err)
        except Exception as err:
            raise CommandError('FAIL: %s' % (err))
