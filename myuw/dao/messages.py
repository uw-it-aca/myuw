import csv
import os
import datetime
from dateutil.parser import parse
from django.conf import settings
from myuw.dao.term import get_comparison_date
from myuw.dao import is_netid_in_list, get_netid_of_current_user
from myuw.models import BannerMessage
from myuw.dao.affiliation import get_all_affiliations
from myuw.dao.affiliation_data import get_data_for_affiliations


"""
Gets the banner message for the current day/quarter
Currently will fetch messages stored in data CSV but could be enhanced to
include an admin interface for storing messages and eligibility.
"""
SAMPLE_LIST = "SAMPLE_LIST"
SAMPLE_PATH = "data/seru_users.txt"


def get_current_messages(request):
    current_date = get_comparison_date(request)
    affiliations = get_all_affiliations(request)

    messages = get_data_for_affiliations(model=BannerMessage,
                                         affiliations=affiliations,
                                         start__lte=current_date,
                                         end__gte=current_date)

    return messages
