from myuw_mobile.user import UserService
from myuw_mobile.logger.timer import Timer
import logging

def log_success_response(logger, timer):
    logger.info("%s - fulfilled. Time=%.2f milliseconds",
                UserService().get_logging_userid(),
                timer.get_elapsed())

def log_data_not_found_response(logger, timer):
    logger.warning("%s - data not found. Time=%.2f milliseconds",
                UserService().get_logging_userid(),
                timer.get_elapsed())

def log_invalid_netid_response(logger, timer):
    logger.error("%s - invalid netid, abort! Time=%.2f milliseconds",
                UserService().get_logging_userid(),
                timer.get_elapsed())

def log_invalid_regid_response(logger, timer):
    logger.error("%s - invalid regid, abort! Time=%.2f milliseconds",
                UserService().get_logging_userid(),
                timer.get_elapsed())

def log_exception(logger, action, message):
    logger.error("%s - %s =>Exception: %s",
                 UserService().get_logging_userid(),
                 action,
                 message)

def log_resp_time(logger, action, timer):
    logger.info("%s - %s fulfilled. Time=%.2f milliseconds",
                UserService().get_logging_userid(),
                action,
                timer.get_elapsed())


