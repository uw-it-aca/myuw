import json
import logging
import re
from base64 import b64decode
from logging import getLogger
from time import time
from math import floor
from aws_message.crypto import aes128cbc, Signature, CryptoException
from restclients_core.exceptions import DataFailureException
from uw_kws import KWS, ENCRYPTION_KEY_URL, ENCRYPTION_CURRENT_KEY_URL
from uw_kws.dao import KWS_DAO
from rc_django.models import CacheEntryTimed
from uw_sws.dao import SWS_DAO
from myuw.dao import is_using_file_dao
from myuw.util.cache_implementation import MyUWMemcachedCache
from myuw.event.exceptions import EventException


myuwcache = MyUWMemcachedCache()
kws = KWS()
SWS_SERVICE_NAME = SWS_DAO().service_name
KWS_SERVICE_NAME = KWS_DAO().service_name

# message body tidy up
re_json_cruft = re.compile(r'[^{]*({.*})[^}]*')

# message body crypto pattern
re_crypto = re.compile(r'^\s*{.+}\s*$')


class EventHandler(object):

    def __init__(self, logger, message,
                 event_message_type=None, is_encrypted=False):
        """
        :param message: a dict representing a UW Course Event Message
        Raises EventException
        """
        self.header = None
        self.body = None
        self.logger = logger
        self.is_encrypted = is_encrypted
        self.message_type = event_message_type
        self.err_msg = "(MESSAGE: %s)" % message

        self.logger.debug(message)
        self.body = message

    def extract(self):
        try:
            if self.is_encrypted:
                body = self.decrypt_message()
            else:
                body = self.body
            return json.loads(re_json_cruft.sub(r'\g<1>', body))
        except Exception as err:
            raise EventException("extract %s ==> %s" % (self.err_msg, err))

    def decrypt_message(self):
        try:
            key = self.get_encryption_key()
            cipher = aes128cbc(b64decode(key.key),
                               b64decode(self.header['IV']))

            # Decrypt the message using the Key
            body = cipher.decrypt(b64decode(self.body))
        except Exception as err:
            raise EventException("decrypt_message %s ==> %s" % (self.err_msg,
                                                                err))

    def get_encryption_key(self):
        """
        Retrieve message body encryption key
        """
        if 'KeyURL' in self.header:
            key_url = self.header.get('KeyURL', None)
            if key_url is not None and len(key_url):
                try:
                    # create an encryption key object with KeyURL
                    return kws._key_from_json(kws._get_resource(key_url))
                except DataFailureException as err:
                    self.logger.error("get_encryption_key by url(%s) ==> %s" %
                                      (key_url, err))

        if 'KeyId' in self.header:
            # get encryption key with KeyId
            key_id = self.header.get('KeyId', None)
            if key_id is not None and len(key_id):
                try:
                    return kws.get_key(key_id)
                except DataFailureException as err:
                    self.logger.error("get_encryption_key by KeyId(%s) ==> %s"
                                      % (key_id, err))

        try:
            # get encryption key with the message type
            key = kws.get_current_key(self.message_type)

            # what is it checking ??
            if not re_crypto.match(self.body):
                raise CryptoException(self.body)

        except (ValueError, CryptoException) as err:
            # clear the cached current key
            clear_cached_kws_current_key(self.message_type)

            try:
                # get a new current key
                return kws.get_current_key(self.message_type)
            except DataFailureException as err:
                msg = "get_encryption_key ==> %s" % err
                self.logger.error(msg)
                raise EventException(msg)

    def validate(self):
        """
        how does this diff from django-aws-message/aws_message/gather 
        SNS.validate()?
        """
        try:
            to_sign = self.header['MessageType'] + '\n' \
                + self.header['MessageId'] + '\n' \
                + self.header['TimeStamp'] + '\n' \
                + self.body + '\n'
            self.logger.info("TO_SIGN=%s" % to_sign)

            sig_conf = {
                'cert': {
                    'type': 'url',
                    'reference': self.header['SigningCertURL']
                }
            }

            Signature(sig_conf).validate(to_sign.encode('ascii'),
                                         b64decode(self.header['Signature']))
        except Exception as err:
            raise EventException("validate %s ==> %s" % (self.err_msg, err))

    def process(self):
        if not is_using_file_dao():
            self.validate()
        self.process_message_content(self.extract())

    def process_message_content(self, message_content_json):
        raise EventException('No event processor defined')


def clear_cached_kws_current_key(resource_type):
    myuwcache.delete_cached_value(KWS_SERVICE_NAME,
                                  ENCRYPTION_CURRENT_KEY_URL % resource_type)


# do you ever need to clear this ENCRYPTION key
def clear_cached_kws_key(key_id):
    myuwcache.delete_cached_value(KWS_SERVICE_NAME,
                                  ENCRYPTION_KEY_URL % key_id)


def clear_cached_sws_entry(url):
    myuwcache.delete_cached_value(SWS_SERVICE_NAME, url)
