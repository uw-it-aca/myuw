import os
from django.conf import settings
from uw_sws.dao import SWS_DAO
from userservice.user import UserService
from myuw.models import User
from uw_pws import PWS


def get_netid_of_current_user():
    return UserService().get_user()


def get_user_model():
    user_netid = get_netid_of_current_user()
    try:
        user = User.objects.get(uwnetid=user_netid, uwregid=None)
    except User.DoesNotExist:
        user_regid = PWS().get_person_by_netid(user_netid).uwregid
        try:
            user = User.objects.get(uwnetid=user_netid, uwregid=user_regid)
        except User.DoesNotExist:
            user = User(uwnetid=user_netid, uwregid=user_regid)
            user.save()

    return user


def is_using_file_dao():
    return SWS_DAO().get_implementation().is_mock()


def _is_optin_user(uwnetid):
    file_path = _get_file_path("MYUW_OPTIN_SWITCH_PATH",
                               "optin-list.txt")

    return is_netid_in_list(uwnetid, file_path)


def is_fyp_thrive_viewer(uwnetid):
    file_path = _get_file_path("MYUW_MANDATORY_SWITCH_PATH",
                               "thrive-viewer-list.txt")

    return is_netid_in_list(uwnetid, file_path)


def _get_file_path(settings_key, default_filename):
    file_path = getattr(settings, settings_key, None)
    if not file_path:
        current_dir = os.path.dirname(os.path.realpath(__file__))

        file_path = os.path.abspath(os.path.join(current_dir,
                                                 "..", "data",
                                                 default_filename))
    return file_path


def is_netid_in_list(username, file_path):
    with open(file_path) as data_source:
        for line in data_source:
            if line.rstrip() == username:
                return True

    return False
