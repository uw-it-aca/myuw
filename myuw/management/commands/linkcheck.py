#!/usr/bin/python
"""
Test all the links in the CSV for non-200 status codes (after redirects).
"""

import sys
import csv
import urllib3

from django.core.management.base import BaseCommand, CommandError

# Need to override UA for some links, e.g. LinkedIn
user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'

# Disable SSL warnings
urllib3.disable_warnings()
# Need limit of 1, otherwise sdb gives us a 403
http = urllib3.PoolManager(1, timeout=8)

# CSV fields
category = 0
subcat = 1
affiliation = 2
links = 3
newtab = links + (2 * 4)
schools = {0: 'Central', 1: 'Seattle', 2: 'Bothell', 3: 'Tacoma'}


class Command(BaseCommand):

    help = ('Automatically check all links in category_links_import.csv'
            'Ensures the links return 200 after redirects.')

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
            headers={'User-Agent': user_agent},
            retries = urllib3.Retry(redirect=10),
        )
        return result.status

    except Exception:
        return repr(sys.exc_info()[1])


class MyuwLink(object):
    """Class for links found in the CSV."""

    def __init__(self, name, url, school='Central'):
        self.name = name
        self.url = url
        self.school = school

    @classmethod
    def from_csv_line(cls, fields):
        """
        Given a line of the CSV, make one of more links out of it, and
        return them as a list.
        """
        # Each CSV line can either be one link (for all campuses), or
        # one line for each campus.

        # Iterate in steps of two
        # Generate 3-tuples of url, name, index (0 = global, 1 = seattle, etc)
        out = []
        for i in xrange(4):
            url = fields[links + 2 * i]
            name = fields[links + 2 * i + 1]
            if url and name:
                school = schools[i]
                out.append(cls(name, url, school))
        return out

    def get_status(self):
        """Get status code of this link's URL."""
        self.status = get_http_status(self.url)
        return self.status


def read_links_from_file(filepath=None):
    '''Read links from the csv file. If path is not specified, try to guess.'''
    guesspaths = [
        # Path for when myuw is installed as a package
        'src/myuw/myuw/data/category_links_import.csv',
        # Path for when myuw is installed at the top level
        'myuw/data/category_links_import.csv'
    ]
    for path in guesspaths:
        try:
            f = open(path, 'r')
            break
        except IOError:
            continue
    else:
        raise Exception('Could not find links file')

    links = []
    reader = csv.reader(f)
    # Ignore first line
    reader.next()
    for line in reader:
        links += MyuwLink.from_csv_line(line)
    f.close()
    return links


def check_and_format(link, ignore=[200]):
    result = link.get_status()
    if result in ignore:
        return None

    else:
        fmt = (link.school, link.name, link.url, result)
        return 'URL (%s) %s (%s) returned %s' % fmt


def check_all():

    links = read_links_from_file()
    for link in links:
        out = check_and_format(link)
        if out is not None:
            print out


if __name__ == '__main__':
    check_all()
