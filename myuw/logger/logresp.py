import json
import logging
from myuw.logger.logback import log_info, log_time, log_exception_with_timer
from myuw.logger.session_log import hash_session_key

resp_logger = logging.getLogger(__name__)


def __log_resptime(timer, action_message):
    resp_logger.info("{} Time={} seconds".format(action_message,
                                                 timer.get_elapsed()))


def log_page_view(timer, request, template_name):
    msg = json.dumps({'page': template_name,
                      'session_key': hash_session_key(request)})
    if timer:
        __log_resptime(timer, msg)
    else:
        resp_logger.info(msg)


def log_api_call(timer, request, message):
    __log_resptime(timer,
                   json.dumps({'api': message,
                               'session_key': hash_session_key(request)}))


def log_interaction(request, interaction_type):
    if interaction_type:
        resp_logger.info(json.dumps(
            {'client-side interaction': interaction_type,
             'session_key': hash_session_key(request)}))


def log_err(logger, timer, exc_info):
    """
    exc_info is a string containing
    the full stack trace, the exception type and value
    """
    log_exception_with_timer(logger, timer, exc_info)


def log_msg(logger, timer, msg):
    log_time(logger, msg, timer)


def log_data_not_found_response(logger, timer):
    log_time(logger, 'Data not found', timer)


def log_invalid_netid_response(logger, timer):
    log_time(logger, 'Invalid netid, abort', timer)


def log_invalid_regid_response(logger, timer):
    log_time(logger, 'Invalid regid, abort', timer)
