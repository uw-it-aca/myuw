from os.path import dirname
import logging
import re
from restclients.dao_implementation.live import get_con_pool, get_live_url
from myuw_mobile.logger.logback import log_info
from restclients.dao_implementation.mock import get_mockdata_url


class File(object):
    """
    This implementation returns mock/static content.
    Use this DAO with this configuration:

    RESTCLIENTS_HFS_DAO_CLASS =
        'myuw_mobile.restclients.dao_implementation.hfs.File'
    """
    def getURL(self, url, headers):
        """
        Return the url for accessing the mock data in local file
        :param url:
            in the format of "hfs/servlet/hfservices?sn=<student number>"
        """
        file_url = re.sub('[\?<>=:,;+&]', '_', url)
        log_info(Live.logger, "HFS File url=%s" % file_url)
        return get_mockdata_url("hfs", "file", file_url, headers)


class Live(object):
    """
    This DAO provides real data.
    Access is restricted to localhost.
    """
    logger = logging.getLogger(__name__)
    pool = None

    def getURL(self, url, headers):
        """
        Return the absolute url for accessing live data
        :param url:
            in the format of "hfs/servlet/hfservices?sn=<student number>"
        """
        host = 'http://localhost:80/'
        if Live.pool is None:
            Live.pool = get_con_pool(host, None, None,
                                     socket_timeout=5.0,
                                     max_pool_size=5)
        log_info(Live.logger, Live.pool)
        return get_live_url(Live.pool, 'GET',
                            host, url, headers=headers)
