# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.core.management.base import BaseCommand, CommandError
from myuw.event.section_status import SectionStatusProcessor
from aws_message.gather import Gather, GatherException
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Loads Section Status change events from SQS
    """
    def handle(self, *args, **options):
        try:
            Gather(processor=SectionStatusProcessor()).gather_events()
        except GatherException as ex:
            logger.error(ex)
            raise CommandError(ex)
