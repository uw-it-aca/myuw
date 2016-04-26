#!/usr/bin/python
"""
Test all the links in the CSV for non-200 status codes (after redirects).
"""

import sys
import urllib3

from django.core.management.base import BaseCommand, CommandError
from myuw.dao.category_links import Res_Links

# Disable SSL warnings
urllib3.disable_warnings()
# Need limit of 1, otherwise sdb gives us a 403
http = urllib3.PoolManager(1, timeout=8)
# Need to override UA for some links, e.g. LinkedIn
ua = 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'


class Command(BaseCommand):

    help = ('Test all resource links for non-200 status codes after'
    ' following redirects')

    def handle(self, *args, **kwargs):
        try:
            check_all()
        except Exception as e:
            raise CommandError(e)


def get_http_status(url):
    """
    Given a url, get the HTTP status code or a human-readable exception.
    """
    try:
        result = http.request(
            'GET',
            url,
            headers={'User-Agent': ua},
            retries = urllib3.Retry(redirect=10, connect=2, read=2)
        )
        return result.status

    except Exception:
        return repr(sys.exc_info()[1])


def check_and_format(link, ignore=[200]):
    result = get_http_status(link.url)

    if result in ignore:
        return None

    else:
        campus = campus_human_readable(link.campus)
        fmt = (campus, link.title, link.url, result)
        return 'URL (%s) %s (%s) returned %s' % fmt


def check_all():

    links = Res_Links.get_all_links()
    for link in links:
        out = check_and_format(link)
        if out is not None:
            print out


def campus_human_readable(campus):

    if campus is None:
        return 'All'
    else:
        # Capitalize first letter
        return campus[0:1].upper() + campus[1:]
