import os
from django.conf import settings
from restclients.dao import SWS_DAO
from userservice.user import UserService
from myuw.models import User


def get_netid_of_current_user():
    return UserService().get_user()


def get_user_model():
    user_netid = get_netid_of_current_user()
    user, created = User.objects.get_or_create(uwnetid=user_netid)
    return user


def is_using_file_dao():
    return SWS_DAO().get_implementation().is_mock()


THRIVE = "thrive"
OPTIN = "optin"


def _is_optin_user(uwnetid):
    return _is_netid_in_list(uwnetid, OPTIN)


def is_fyp_thrive_viewer(uwnetid):
    return _is_netid_in_list(uwnetid, THRIVE)


def _is_netid_in_list(username, user_type):
    if THRIVE == user_type:
        file_path = getattr(settings, "MYUW_MANDATORY_SWITCH_PATH", None)
        if not file_path:
            current_dir = os.path.dirname(os.path.realpath(__file__))

            file_path = os.path.abspath(os.path.join(current_dir,
                                                     "..", "data",
                                                     "thrive-viewer-list.txt"))

    else:
        file_path = getattr(settings, "MYUW_OPTIN_SWITCH_PATH", None)
        if not file_path:
            current_dir = os.path.dirname(os.path.realpath(__file__))

            file_path = os.path.abspath(os.path.join(current_dir,
                                                     "..", "data",
                                                     "optin-list.txt"))

    with open(file_path) as data_source:
        for line in data_source:
            if line.rstrip() == username:
                return True

    return False
