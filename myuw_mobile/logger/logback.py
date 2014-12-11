import logging
from userservice.user import UserService
from myuw_mobile.logger.timer import Timer


def log_exception(logger, action, exc_info):
    """
    exc_info is a string containing
    the full stack trace, the exception type and value
    """
    logger.error("%s - %s => %s ",
                 get_logging_userid(),
                 action,
                 exc_info.splitlines())


def log_info(logger, message):
    logger.info("%s %s", get_logging_userid(), message)


def log_time(logger, action_message, timer):
    log_info(logger,
             "%s Time=%.3f milliseconds" %
             (action_message, timer.get_elapsed())
             )


def log_resp_time(logger, action, timer):
    log_time(logger,
             action + ' fulfilled',
             timer)


def get_logging_userid():
    """
    Return <actual user netid> acting_as: <override user netid> if
    the user is acting as someone else, otherwise
    <actual user netid> no_override: <actual user netid>
    """
    user_svc = UserService()
    override_userid = user_svc.get_override_user()
    actual_userid = user_svc.get_original_user()
    log_format = 'base_user: %s acting_user: %s is_override: %s'
    try:
        if override_userid:
            log_userid = log_format % (actual_userid, override_userid, 'true')
        else:
            log_userid = log_format % (actual_userid, actual_userid, 'false')
    except TypeError:
        return None
    return log_userid
