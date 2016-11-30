import logging
import os
from django.conf import settings
from myuw.models import UserMigrationPreference
from myuw.dao.pws import get_netid_of_current_user
from myuw.dao.gws import is_staff_employee, is_student_employee,\
    is_undergrad_student, is_current_graduate_student, is_employee, is_faculty


THRIVE = "thrive"
OPTIN = "optin"
logger = logging.getLogger(__name__)


def set_preference_to_new_myuw(uwnetid):
    obj, is_new = UserMigrationPreference.objects.get_or_create(
        username=uwnetid)
    obj.use_legacy_site = False
    obj.save()


def set_preference_to_old_myuw(uwnetid):
    obj, is_new = UserMigrationPreference.objects.get_or_create(
        username=uwnetid)
    obj.use_legacy_site = True
    obj.save()


def has_legacy_preference(uwnetid):
    try:
        saved = UserMigrationPreference.objects.get(username=uwnetid)
        if saved.use_legacy_site:
            return True
    except UserMigrationPreference.DoesNotExist:
        pass
    return False


def has_newmyuw_preference(uwnetid):
    try:
        saved = UserMigrationPreference.objects.get(username=uwnetid)
        if saved and not saved.use_legacy_site:
            return True
    except UserMigrationPreference.DoesNotExist:
        pass
    return False


def is_oldmyuw_user():
    uwnetid = get_netid_of_current_user()
    if has_legacy_preference(uwnetid):
        return True
    if is_optin_user(uwnetid) or has_newmyuw_preference(uwnetid):
        return False
    if is_staff_employee():
        return True
    if is_faculty():
        return True
    if is_current_graduate_student():
        return True
    if is_undergrad_student():
        return False
    return True


def is_optin_user(uwnetid):
    return _is_user_in_list(uwnetid, OPTIN)


def is_fyp_thrive_viewer(uwnetid):
    return _is_user_in_list(uwnetid, THRIVE)


def _is_user_in_list(username, user_type):
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
