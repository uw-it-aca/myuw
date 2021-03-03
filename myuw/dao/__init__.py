import logging
import os
from django.conf import settings
from uw_sws import DAO as SWS_DAO
from userservice.user import (
    UserService, get_user, get_original_user)
from myuw.util.settings import get_disable_actions_when_override

logger = logging.getLogger(__name__)
disable_actions_when_override = get_disable_actions_when_override()


def get_netid_of_current_user(request=None):
    """
    return the over-ride user if impersonated
    """
    if request:
        return get_user(request)
    return UserService().get_user()


def get_netid_of_original_user(request=None):
    """
    return the actual authenticated user
    """
    if request:
        return get_original_user(request)
    return UserService().get_original_user()


def get_userids(request=None):
    """
    Return a dict of {orig_netid: netid,
                      acting_netid: netid,
                      is_override: True/False}
    """
    user = None
    orig_userid = None
    try:
        user = get_netid_of_current_user(request)
        orig_userid = get_netid_of_original_user(request)
    except Exception:
        pass
    return {'acting_netid': user,
            'orig_netid': orig_userid,
            'is_override': (user is not None and
                            orig_userid is not None and
                            user != orig_userid)}


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


def _get_file_path(settings_key, filename):
    file_path = getattr(settings, settings_key, None)
    if file_path:
        return os.path.join(file_path, filename)

    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.abspath(os.path.join(current_dir,
                                             "..", "data",
                                             filename))
    return file_path


def log_err(logger, msg_str, stacktrace, request):
    logger.error(
        {**get_userids(request=request),
         **{'at': msg_str,
            'err': stacktrace.format_exc(chain=False).splitlines()}})
