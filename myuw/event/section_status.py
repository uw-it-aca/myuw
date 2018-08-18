"""
Handle SWS Section Status events
https://wiki.cac.washington.edu/x/sNFdB
"""

import logging
from datetime import timedelta
from django.utils import timezone
from dateutil.parser import parse
from uw_sws import encode_section_label
from myuw.event import EventHandler, clear_cached_sws_entry
from myuw.event.exceptions import EventException

logger = logging.getLogger(__name__)
message_freshness = timedelta(hours=1)


class SectionStatusEventHandler(EventHandler):

    SETTINGS_NAME = 'SECTION_SATSUS_V1'
    EXCEPTION_CLASS = EventException

    def __init__(self, message):
        super(SectionStatusEventHandler, self).__init__(logger, message)

    def process_message_content(self, message_content_json):
        """
        Each status change message body contains a single event
        """
        print message_content_json
        if 'EventDate' in message_content_json:
            modified = parse(message_content_json['EventDate'])
            # 2018-08-12T14:18:41.3136155-07:00
            if modified <= (timezone.now() - message_freshness):
                logger.info("Discard old message: %s" % message_content_json)
                return

            if 'Href' in message_content_json:
                status_url = message_content_json['Href']
                # /v5/course/2018,autumn,SOC,225/A/status.json

                # current = message_content_json['Current']
                self.clear_cache(status_url)

    def clear_cache(self, status_url, time_stamp):
        url = "/student/%s" % status_url
        clear_cached_sws_entry(url)
        logger.info("Cleared section status from cache (%s)", url)
