"""
Test all the links in the CSV for non-200 status codes (after redirects).
"""

import logging
import sys
import urllib3
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from myuw.dao.category_links import Res_Links
from myuw.util.settings import get_cronjob_recipient, get_cronjob_sender

# Disable SSL warnings
urllib3.disable_warnings()
# Need limit of 1, otherwise sdb gives us a 403
http = urllib3.PoolManager(1, timeout=8)
# Need to override UA for some links, e.g. LinkedIn
ua = 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        messages = []
        links = Res_Links.get_all_links()
        for link in links:
            if link.url.startswith("https://sdb."):
                continue
            status = get_http_status(link.url, messages)
            if status not in [200]:
                msg = "{}, {}, URL: {} =status=> {}\n\n".format(
                    link.title, make_campus_human_readable(link.campus),
                    link.url, status)
                logger.error(msg)
                messages.append(msg)
        if len(messages):
            send_mail("Check Cetegory Links Cron",
                      "\n".join(messages),
                      "{}@uw.edu".format(get_cronjob_sender()),
                      ["{}@uw.edu".format(get_cronjob_recipient())])


def get_http_status(url, messages):
    """
    Given a url, get the HTTP status code or a human-readable exception.
    """
    try:
        result = http.request(
            'GET',
            url,
            headers={'User-Agent': ua},
            retries=urllib3.Retry(redirect=1, connect=2, read=2)
        )
        return result.status
    except Exception as ex:
        messages.append(str(ex))


def make_campus_human_readable(campus):

    if campus is None:
        return 'All Campuses'
    else:
        # Capitalize first letter
        return campus[0:1].upper() + campus[1:]
