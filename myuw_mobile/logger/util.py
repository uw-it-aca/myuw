from myuw_mobile.user import UserService
from myuw_mobile.logger.timer import Timer
import logging

def log_success_response(logger, user_service, timer):
    logger.info("%s - fulfilled. time=%.2f",
                user_service.get_logging_userid(),
                timer.get_elapsed())

def log_data_not_found_response(logger, user_service, timer):
    logger.warning("%s - data not found. time=%.2f",
                user_service.get_logging_userid(),
                timer.get_elapsed())

def log_invalid_netid_response(logger, user_service, timer):
    logger.error("%s - invalid netid, abort! time=%.2f",
                user_service.get_logging_userid(),
                timer.get_elapsed())

def log_invalid_regid_response(logger, user_service, timer):
    logger.error("%s - invalid regid, abort! time=%.2f",
                user_service.get_logging_userid(),
                timer.get_elapsed())

def log_resp_time(logger, user_service, action, timer):
    logger.error("%s - %s. time=%.2f",
                 user_service.get_logging_userid(),
                 action,
                 timer.get_elapsed())

def log_exception(logger, user_service, action, message):
    logger.error("%s - %s =>Exception: %s",
                 user_service.get_logging_userid(),
                 action,
                 message)


