from myuw_mobile.user import UserService
from myuw_mobile.logger.timer import Timer
import logging

def log_success_response(logger, user_service, timer):
    logger.info("%s - fulfilled. time=%f",
                user_service.get_logging_userid(),
                timer.get_elapsed())

def log_data_not_found_response(logger, user_service, timer):
    logger.warning("%s - data not found. time=%f",
                user_service.get_logging_userid(),
                timer.get_elapsed())

def log_invalid_netid_response(logger, user_service, timer):
    logger.error("%s - invalid netid, abort! time=%f",
                user_service.get_logging_userid(),
                timer.get_elapsed())

def log_invalid_regid_response(logger, user_service, timer):
    logger.error("%s - invalid regid, abort! time=%f",
                user_service.get_logging_userid(),
                timer.get_elapsed())

def log_exception(logger, user_service, message, timer):
    logger.error("%s - Exception: %s. time=%f",
                 user_service.get_logging_userid(),
                 message,
                 timer.get_elapsed())



