"""
This module provides access to instructed class website
"""

import logging
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup
from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.dao_implementation.mock import get_mockdata_url
from restclients.exceptions import DataFailureException
from myuw.dao import is_using_file_dao
import re

logger = logging.getLogger(__name__)


def _fetch_url(method, url):
    try:
        p = urlparse(url)
    except Exception as ex:
        logger.error("_get_html_from_url(%s)==>%s" % (url, ex))
        return None

    headers = {'ACCEPT': 'text/html'}
    if is_using_file_dao():
        response = get_mockdata_url(
            'www', 'file', "/%s%s" % (p.netloc, p.path), headers)
    else:
        pool = get_con_pool("%s://%s" % (p.scheme, p.netloc), socket_timeout=2)
        response = get_live_url(
            pool, method, p.hostname, url, headers)

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
