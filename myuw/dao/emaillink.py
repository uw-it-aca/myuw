"""
This class encapsulates the mapping between
email address and service provider login
"""

import re
import os
import csv
from myuw.dao.exceptions import EmailServiceUrlException


def get_service_url_for_address(address):
    path = os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'forward_mapping.csv')

    with open(path, 'rbU') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        # skip header
        next(reader)
        for row in reader:
            try:
                if re.match('.*[@\.]%s$' % row[0], address, re.I):
                    return (row[1], row[2], row[3])
            except TypeError:
                raise EmailServiceUrlException("Non-string address")

    raise EmailServiceUrlException()
