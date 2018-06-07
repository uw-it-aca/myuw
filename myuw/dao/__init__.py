import logging
import os
import io
from django.conf import settings
from uw_sws import DAO as SWS_DAO
from userservice.user import UserService
from myuw.util.settings import get_disable_actions_when_override


logger = logging.getLogger(__name__)
disable_actions_when_override = get_disable_actions_when_override()


def get_netid_of_current_user(request=None):
    """
    return the over-ridden user if impersonated
    """
    if request is None:
        return UserService().get_user()

    if not hasattr(request, "myuwnetid"):
        request.myuwnetid = UserService().get_user()
    return request.myuwnetid


def get_netid_of_original_user():
    """
    return the actual authenticated user
    """
    return UserService().get_original_user()


def is_action_disabled():
    """
    return True if overriding and
    MYUW_DISABLE_ACTIONS_WHEN_OVERRIDE is True
    """
    overrider = UserService().get_override_user()
    disable_actions_when_override = get_disable_actions_when_override()
    return disable_actions_when_override and overrider is not None


def is_using_file_dao():
    return SWS_DAO.get_implementation().is_mock()


def is_thrive_viewer(uwnetid, population):
    file_path = _get_file_path("MYUW_MANDATORY_SWITCH_PATH",
                               population + "_list.txt")
    return is_netid_in_list(uwnetid, file_path)


def _get_file_path(settings_key, filename):
    file_path = getattr(settings, settings_key, None)
    if file_path:
        return os.path.join(file_path, filename)

    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.abspath(os.path.join(current_dir,
                                             "..", "data",
                                             filename))
    return file_path


def is_netid_in_list(username, file_path):
    netid = username.decode('utf8')
    with io.open(file_path, 'r', encoding='utf8') as data_source:
        for line in data_source:
            try:
                if line.rstrip() == netid:
                    return True
            except Exception as ex:
                logger.error("%s: %s==%s", ex, line, username)

    return False
