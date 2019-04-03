"""
Handle SWS Section Status events
https://wiki.cac.washington.edu/x/sNFdB
"""

import logging
from datetime import timedelta
import traceback
from django.utils import timezone
from dateutil.parser import parse
from aws_message.processor import MessageBodyProcessor, ProcessorException
from myuw.logger.logresp import log_exception
from myuw.event import update_sws_entry_in_cache


logger = logging.getLogger(__name__)
MESSAGE_FRESHNESS = timedelta(hours=4)
QUEUE_SETTINGS_NAME = 'SECTION_SATSUS_V1'


class SectionStatusProcessorException(ProcessorException):
    pass


class SectionStatusProcessor(MessageBodyProcessor):

    EXCEPTION_CLASS = SectionStatusProcessorException

    def __init__(self, queue_settings_name=QUEUE_SETTINGS_NAME):
        super(SectionStatusProcessor, self).__init__(logger,
                                                     queue_settings_name)

    def validate_message_body(self, payload):
        """
        This method will be called before process_message_body.
        Return False if payload json data misses any necessary
        data element and the message will be skipped.
        """
        if (payload is None or
                payload.get('EventDate') is None):
            return False

        self.modified = parse(payload['EventDate'])
        if self.modified <= (timezone.now() - MESSAGE_FRESHNESS):
            logger.debug("DISCARD Old message {}".format(payload))
            return False

        if (payload.get('Current') is None or
                len(payload.get('Current')) == 0 or
                payload.get('Href') is None or
                len(payload.get('Href')) == 0):
            logger.error("DISCARD Bad message {}".format(payload))
            return False

        return True

    def process_message_body(self, payload):
        # payload['Href']: /v5/course/2018,autumn,SOC,225/A/status.json
        url = "/student{}".format(payload['Href'])
        new_value = payload['Current']

        try:
            update_sws_entry_in_cache(url, new_value, self.modified)
        except Exception:
            msg = "Updating memcache failed on {}, {}".format(url,
                                                              new_value)
            log_exception(logger, msg, traceback.format_exc())
            raise SectionStatusProcessorException(msg)
