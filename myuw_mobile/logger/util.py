from myuw_mobile.user import UserService
from myuw_mobile.logger.timer import Timer
import logging

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

def log_success_response(logger, timer):
    logger.info("%s - fulfilled. Time=%d microseconds",
                get_logging_userid(),
                timer.get_elapsed())

def log_data_not_found_response(logger, timer):
    logger.warning("%s - data not found. Time=%d microseconds",
                get_logging_userid(),
                timer.get_elapsed())

def log_invalid_netid_response(logger, timer):
    logger.error("%s - invalid netid, abort! Time=%d microseconds",
                get_logging_userid(),
                timer.get_elapsed())

def log_invalid_regid_response(logger, timer):
    logger.error("%s - invalid regid, abort! Time=%d microseconds",
                get_logging_userid(),
                timer.get_elapsed())

def log_exception(logger, action, message):
    logger.error("%s - %s =>Exception: %s",
                 get_logging_userid(),
                 action,
                 message)

def log_resp_time(logger, action, timer):
    logger.info("%s - %s end. Time=%d microseconds",
                get_logging_userid(),
                action,
                timer.get_elapsed())


