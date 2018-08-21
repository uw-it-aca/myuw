"""
Handle SWS Section Status events
https://wiki.cac.washington.edu/x/sNFdB
"""

import logging
from datetime import timedelta
from django.utils import timezone
from dateutil.parser import parse
from aws_message.processor import InnerMessageProcessor, ProcessorException
from myuw.event import clear_cached_sws_entry


logger = logging.getLogger(__name__)
message_freshness = timedelta(days=1)
QUEUE_SETTINGS_NAME = 'SECTION_SATSUS_V1'


class SectionStatusProcessorException(ProcessorException):
    pass


class SectionStatusProcessor(InnerMessageProcessor):

    EXCEPTION_CLASS = SectionStatusProcessorException

    def __init__(self):
        super(SectionStatusProcessor, self).__init__(
            logger, queue_settings_name=QUEUE_SETTINGS_NAME)

    def process_inner_message(self, json_data):
        """
        Each status change message body contains a single event
        """
        if 'EventDate' in json_data:
            modified = parse(json_data['EventDate'])
            if modified <= (timezone.now() - message_freshness):
                logger.info("DISCARD (EventDate: %s)", modified)
                return

            if 'Href' in json_data:
                status_url = json_data['Href']
                # /v5/course/2018,autumn,SOC,225/A/status.json

                # current = json_data['Current']
                self.clear_cache(status_url)
                logger.info("Message %s is processed!", json_data)

    def clear_cache(self, status_url, time_stamp):
        url = "/student/%s" % status_url
        clear_cached_sws_entry(url)
        logger.info("Cleared section status from cache (%s)", url)
