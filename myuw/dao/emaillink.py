# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

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

    with open(path, 'r', encoding='utf8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        # skip header
        next(reader)
        for row in reader:
            try:
                if re.match(r'.*[@\.]{}$'.format(row[0]), address, re.I):
                    return row[1]
            except TypeError:
                raise EmailServiceUrlException("Non-string address")

    raise EmailServiceUrlException()
