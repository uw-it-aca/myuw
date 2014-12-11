"""
A subclass of the SWS file implementation, allows for specifying the current
week of the term
"""

from restclients.dao_implementation.sws import File, Live
from restclients.mock_http import MockHTTP
from django.conf import settings
from datetime import datetime, timedelta
import json
import re


class ByWeek(File):
    pass


class ByWeekLive(Live):
    pass
