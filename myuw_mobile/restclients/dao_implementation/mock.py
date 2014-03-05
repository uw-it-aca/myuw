from os.path import abspath, dirname
import logging
from restclients.mock_http import MockHTTP

"""
A local the mock data access
"""

def get_mockdata_url(service_name, implementation_name, 
                     url, headers,
                     dir_base=dirname(__file__)):
    """
    The service_name is somthing like "sws", "pws", "book", "hfs"
    The implementation_name is somthing like "file", etc.
    """
    logger = logging.getLogger(__name__)

    RESOURCE_ROOT = abspath(dir_base + "/../resources/" +
                            service_name + "/" + implementation_name)
    if url == "///":
        # Just a placeholder to put everything else in an else.
        # If there are things that need dynamic work, they'd go here
        pass
    else:
        try:
            handle = open(RESOURCE_ROOT + url)
        except IOError:
            logger.exception("***IOError*** when open(%s%s)" % (RESOURCE_ROOT, url))
            try:
                handle = open(RESOURCE_ROOT + url + "/index.html")
            except IOError:
                response = MockHTTP()
                response.status = 404
                return response

        response = MockHTTP()
        response.status = 200
        response.data = handle.read()
        response.headers = { 
            "X-Data-Source": service_name + " file mock data", 
            }
        return response
