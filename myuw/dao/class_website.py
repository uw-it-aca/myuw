"""
This module provides access to instructed class website
"""

import logging
import traceback
import os
import urllib3
from django.conf import settings
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup
from restclients_core.exceptions import DataFailureException
from restclients_core.dao import DAO
from os.path import abspath, dirname


logger = logging.getLogger(__name__)


class CLASS_WEBSITE_DAO(DAO):
    def __init__(self):
        settings.RESTCLIENTS_WWW_VERIFY_HTTPS = False
        settings.RESTCLIENTS_WWW_CERT_FILE = None
        settings.RESTCLIENTS_WWW_KEY_FILE = None

    def service_name(self):
        return "www"

    def service_mock_paths(self):
        return [abspath(os.path.join(dirname(__file__), "resources"))]

    def getURL(self, url, headers={}):
        try:
            p = urlparse(url)
        except Exception as ex:
            log_exception(logger, "urlparse(%s)" % url,
                          traceback.format_exc())
            return None

        if self.get_implementation().is_mock():
            settings.RESTCLIENTS_WWW_HOST = p.netloc
            url = "/%s%s" % (p.netloc, p.path)
            return self._load_resource("GET", url, headers, None)
        else:
            try:
                http = urllib3.PoolManager()
                return http.request('GET', p.geturl())
            except Exception:
                log_exception(logger, "getURL(%s)" % p.geturl(),
                              traceback.format_exc())
        return None


def _fetch_url(url):
    headers = {'ACCEPT': 'text/html'}
    dao = CLASS_WEBSITE_DAO()
    response = dao.getURL(url, headers)
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
        _fetch_url(url)
        return True
    except Exception as ex:
        pass

    return False
