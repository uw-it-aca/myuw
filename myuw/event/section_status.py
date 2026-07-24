# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from dateutil.parser import parse
from aws_message.processor import MessageBodyProcessor, ProcessorException
from memcached_clients.restclient import CachedHTTPResponse
from myuw.util.cache import MyUWMemcachedCache
import traceback
import logging

logger = logging.getLogger(__name__)
QUEUE_SETTINGS_NAME = 'SECTION_STATUS_V1'


class SectionStatusProcessorException(ProcessorException):
    pass


class SectionStatusProcessor(MessageBodyProcessor):
    """
    Process SWS Section Status events
    https://wiki.cac.washington.edu/x/sNFdB
    """

    _eventMessageType = 'uw-student-section-status-prod-myuw'
    _eventMessageVersion = '1'

    def __init__(self, queue_settings_name=QUEUE_SETTINGS_NAME):
        super(SectionStatusProcessor, self).__init__(logger,
                                                     queue_settings_name)

    def validate_message_body(self, message):
        header = message.get('Header', {})
        if ('MessageType' in header and
                header['MessageType'] != self._eventMessageType):
            raise SectionStatusProcessorException(
                'Unknown Message Type: {}'.format(header['MessageType']))

        if ('Version' in header and
                header['Version'] != self._eventMessageVersion):
            raise SectionStatusProcessorException(
                'Unknown Version: {}'.format(header['Version']))

        return True

    def process_message_body(self, json_data):
        cache_client = MyUWMemcachedCache()
        response = CachedHTTPResponse(status=200, data=json_data['Current'])
        try:
            cache_client.updateCache('sws', json_data['Href'], response)
        except Exception as ex:
            msg = {
                "svc": QUEUE_SETTINGS_NAME,
                "url": json_data['Href'],
                "data": json_data['Current'],
                "err": ex,
            }
            logger.error(msg)
            raise SectionStatusProcessorException(msg)
