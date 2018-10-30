"""
Handle SWS Section Status events
https://wiki.cac.washington.edu/x/sNFdB
"""

import logging
from datetime import timedelta
import traceback
from django.utils import timezone
from dateutil.parser import parse
from aws_message.processor import InnerMessageProcessor, ProcessorException
from myuw.logger.logresp import log_exception
from myuw.event import update_sws_entry_in_cache


logger = logging.getLogger(__name__)
MESSAGE_FRESHNESS = timedelta(hours=4)
QUEUE_SETTINGS_NAME = 'SECTION_SATSUS_V1'


class SectionStatusProcessorException(ProcessorException):
    pass


class SectionStatusProcessor(InnerMessageProcessor):

    EXCEPTION_CLASS = SectionStatusProcessorException

    def __init__(self, queue_settings_name=QUEUE_SETTINGS_NAME):
        super(SectionStatusProcessor, self).__init__(logger,
                                                     queue_settings_name)

    def validate_inner_message(self, message):
        """
        Will be called before process_inner_message.
        return False if json_data in the message body misses any
        necessary data element and the message should be deleted.
        """
        json_data = message
        if 'EventDate' not in json_data:
            return False

        self.modified = parse(json_data['EventDate'])
        if self.modified <= (timezone.now() - MESSAGE_FRESHNESS):
            logger.debug("DISCARD Old message {}".format(json_data))
            return False

        if ('Current' not in json_data or 'Href' not in json_data or
                json_data.get('Current') is None or
                json_data.get('Href') is None):
            logger.error("DISCARD Bad message {}".format(json_data))
            return False

        return True

    def process_inner_message(self, json_data):
        # json_data['Href']: /v5/course/2018,autumn,SOC,225/A/status.json
        url = "/student%s" % json_data['Href']
        new_value = json_data['Current']

        try:
            update_sws_entry_in_cache(url, new_value, self.modified)
        except Exception:
            msg = "Updating memcache failed on {}, {}".format(url,
                                                              new_value)
            log_exception(logger, msg, traceback.format_exc())
            raise SectionStatusProcessorException(msg)
