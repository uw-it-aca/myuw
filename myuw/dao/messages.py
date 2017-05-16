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


def get_filtered_messages(current_date, user):
    messages = _get_messages()
    filtered_messages = []
    for message in messages:

        if message.start <= current_date <= message.end:
            # add support for additional eligibility types here
            if message.eligibility_type == "netid":
                path = _get_netid_file_path(message.eligibility_data)
                try:
                    if is_netid_in_list(user, path):
                        filtered_messages.append(message)
                except (IOError, TypeError) as ex:
                    pass
            else:
                raise NotImplemented("eligibility type filter missing")
    return filtered_messages


def _get_messages():
    path = os.path.join(
        os.path.dirname(__file__),
        '..', 'data', 'banner_message.csv')
    messages = []
    with open(path, 'rbU') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        # skip headers
        next(reader)
        for row in reader:
            message = BannerMessage.from_csv(row)
            messages.append(message)
    return messages


def _get_netid_file_path(filename):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    if filename == SAMPLE_LIST:
        file_path = os.path.abspath(os.path.join(current_dir,
                                                 "..",
                                                 SAMPLE_PATH))
    else:
        file_path = getattr(settings, filename, None)
    return file_path
