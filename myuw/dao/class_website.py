"""
This module provides access to instructed class website
"""

import logging
import traceback
import os
from os.path import abspath, dirname
import urllib3
from django.conf import settings
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup
from restclients_core.exceptions import DataFailureException
from restclients_core.dao import DAO
from myuw.dao import is_using_file_dao


logger = logging.getLogger(__name__)


class CLASS_WEBSITE_DAO(DAO):
    def __init__(self):
        settings.RESTCLIENTS_WWW_VERIFY_HTTPS = False
        settings.RESTCLIENTS_WWW_CERT_FILE = None
        settings.RESTCLIENTS_WWW_KEY_FILE = None
        settings.RESTCLIENTS_WWW_TIMEOUT = 30
        settings.RESTCLIENTS_WWW_POOL_SIZE = 30

        settings.RESTCLIENTS_WWW_DAO_CLASS =\
            getattr(settings, 'RESTCLIENTS_WWW_DAO_CLASS',
                    'Mock' if is_using_file_dao() else 'Live')

    def service_name(self):
        return "www"

    def service_mock_paths(self):
        return [abspath(os.path.join(dirname(__file__), "resources"))]

    def getURL(self, url, headers={'ACCEPT': 'text/html'}):
        try:
            p = urlparse(url)
        except Exception as ex:
            log_exception(logger, "urlparse(%s)" % url,
                          traceback.format_exc())
            return None

        if self.get_implementation().is_mock():
            url = "/%s%s" % (p.netloc, p.path)
        else:
            settings.RESTCLIENTS_WWW_HOST = "%s://%s" % (p.scheme, p.netloc)
            url = p.path
        return self._load_resource("GET", url, headers, None)


def _fetch_url(url):
    response = CLASS_WEBSITE_DAO().getURL(url)
    if response is None:
        return None

    if response.status != 200:
        logger.error("fetch_url %s ==> %s", url, response.status)
        raise DataFailureException(url, response.status, response.data)
    return response.data


def get_page_title_from_url(url):
    try:
        html = _fetch_url(url)
        if html:
            soup = BeautifulSoup(html)
            return soup.title.string
    except AttributeError:
        pass
    except DataFailureException as ex:
        raise
    except Exception as ex:
        logger.error("get_page_title_from_url(%s)==>%s" % (url, ex))

    return None


def is_valid_page_url(url):
    try:
        return _fetch_url(url) is not None
    except Exception as ex:
        log_exception(logger, "is_valid_page_url(%s)" % url,
                      traceback.format_exc())
    return False
