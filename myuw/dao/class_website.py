"""
This module provides access to instructed class website
"""

import logging
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup
from restclients.dao_implementation.live import get_con_pool, get_live_url
from restclients.exceptions import DataFailureException


logger = logging.getLogger(__name__)


def _fetch_url(method, url):
    try:
        p = urlparse(url)
    except Exception as ex:
        logger.error("_get_html_from_url(%s)==>%s" % (url, ex))
        return None

    pool = get_con_pool("%s://%s" % (p.scheme, p.netloc), socket_timeout=2)
    response = get_live_url(
        pool, method, p.hostname, url, {'ACCEPT': 'text/html'})

    if response.status != 200:
        raise DataFailureException(url, response.status, response.data)

    return response.data


def get_page_title_from_url(url):
    try:
        html = _fetch_url('GET', url)
        soup = BeautifulSoup(html)
        return soup.title.string
    except DataFailureException as ex:
        logger.error("get_page_title_from_url(%s)==>%s" % (url, ex))


def is_live_url(url):
    try:
        _fetch_url('HEAD', url)
        return True
    except DataFailureException:
        pass

    return False
