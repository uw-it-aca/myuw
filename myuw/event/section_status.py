# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging

from aws_message.processor import MessageBodyProcessor, ProcessorException
from memcached_clients.restclient import CachedHTTPResponse

from myuw.util.cache import MyUWMemcachedCache

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
    _eventService = 'sws'

    def __init__(self, queue_settings_name=QUEUE_SETTINGS_NAME):
        super().__init__(logger, queue_settings_name)

    def validate_message_body(self, message):
        header = message.get('Header', {})
        if ('MessageType' in header and
                header['MessageType'] != self._eventMessageType):
            raise SectionStatusProcessorException(
                f"Unknown Message Type: {header['MessageType']}")

        if ('Version' in header and
                header['Version'] != self._eventMessageVersion):
            raise SectionStatusProcessorException(
                f"Unknown Version: {header['Version']}")

        return True

    def process_message_body(self, json_data):
        url = json_data.get('Href')
        content = json_data.get('Current')

        if not (url and content):
            raise SectionStatusProcessorException(f"Missing data: {json_data}")

        response = CachedHTTPResponse(status=200, data=content)

        MyUWMemcachedCache().updateCache(self._eventService, url, response)
