import logging
import os
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


def get_netid_of_original_user(request=None):
    """
    return the actual authenticated user
    """
    if request is None:
        return UserService().get_original_user()

    if not hasattr(request, "myuw_orig_netid"):
        request.myuw_orig_netid = UserService().get_original_user()
    return request.myuw_orig_netid


def get_userids(request=None):
    """
    Return <actual user netid> acting_as: <override user netid> if
    the user is acting as someone else, otherwise
    <actual user netid> no_override: <actual user netid>
    """
    lformat = 'orig_netid: {}, acting_netid: {}, is_override: {}'
    try:
        override_userid = get_netid_of_current_user(request)
        actual_userid = get_netid_of_original_user(request)
        return lformat.format(actual_userid,
                              override_userid,
                              override_userid != actual_userid)
    except Exception as ex:
        logger.warning({'get_userids': ex})
    return ""


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


def log_err(logger, msg, stacktrace, request):
    logger.error("{}, {} => {} ".format(
        get_userids(request=request), msg,
        stacktrace.format_exc(chain=False).splitlines()))
