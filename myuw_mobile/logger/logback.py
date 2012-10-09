import logging
from myuw_mobile.user import UserService
from myuw_mobile.logger.timer import Timer

def log_exception(logger, action, message):
    logger.error("%s - %s =>Exception: %s",
                 get_logging_userid(),
                 action,
                 message)

def log_time(logger, action_message, timer):
    logger.info("%s %s. Time=%.3f milliseconds",
                get_logging_userid(),
                action_message,
                timer.get_elapsed())

def log_resp_time(logger, action, timer):
    log_time(logger,
             action + ' fulfilled',
             timer)


def get_logging_userid():
    """
    Return <actual user netid> acting_as: <override user netid> if
    the user is acting as someone else, otherwise <actual user netid>
    """
    user_svc = UserService()
    override_userid = user_svc.get_override_user()
    actual_userid = user_svc.get_original_user()
    if override_userid:
        log_userid = actual_userid + ' acting_as: ' + override_userid
    else:
        log_userid = actual_userid
    return log_userid

