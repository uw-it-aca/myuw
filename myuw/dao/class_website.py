"""
This module provides access to instructed class website
"""

import logging
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup
from restclients_core.exceptions import DataFailureException
from myuw.dao import is_using_file_dao
from restclients_core.dao import DAO
import re

logger = logging.getLogger(__name__)


class CLASS_WEBSITE_DAO(DAO):
    def service_name(self):
        return "www"

    def service_mock_paths(self):
        return [abspath(os.path.join(dirname(__file__), "resources"))]


def _fetch_url(method, url):
    try:
        p = urlparse(url)
    except Exception as ex:
        logger.error("_get_html_from_url(%s)==>%s" % (url, ex))
        return None

    headers = {'ACCEPT': 'text/html'}
    response = CLASS_WEBSITE_DAO().getURL(p, headers)

    if response.status != 200:
        raise DataFailureException(url, response.status, response.data)

    return response.data


def get_page_title_from_url(url):
    try:
        html = _fetch_url('GET', url)
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
        _fetch_url('HEAD', url)
        return True
    except Exception as ex:
        pass

    return False
