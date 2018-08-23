"""
Handle SWS Section Status events
https://wiki.cac.washington.edu/x/sNFdB
"""

import logging
from datetime import timedelta
from django.utils import timezone
from dateutil.parser import parse
from aws_message.processor import InnerMessageProcessor, ProcessorException
from myuw.event import update_sws_entry_in_cache


logger = logging.getLogger(__name__)
message_freshness = timedelta(hours=1)
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
                logger.info("DISCARD Event (Date: %s, ID: %s)",
                            modified, json_data['EventID'])
                return

            status_url = json_data.get('Href')
            # ie, /v5/course/2018,autumn,SOC,225/A/status.json

            new_value = json_data.get('Current')

            if status_url and new_value:
                url = "/student%s" % status_url
                try:
                    update_sws_entry_in_cache(url, new_value, modified)
                except Exception as e:
                    msg = "FAILED to update cache(url=%s) ==> %s" % (url, e)
                    logger.error(msg)
                    raise SectionStatusProcessorException(msg)
