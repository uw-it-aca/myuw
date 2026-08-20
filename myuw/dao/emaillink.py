# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This class encapsulates the mapping between
email address and service provider login
"""

import csv
import os
import re

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
                if re.match(rf'.*[@\.]{row[0]}$', address, re.IGNORECASE):
                    return row[1]
            except TypeError:
                raise EmailServiceUrlException("Non-string address")

    raise EmailServiceUrlException()
