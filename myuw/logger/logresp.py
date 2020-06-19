import logging
from myuw.logger.session_log import hash_session_key
from myuw.dao import get_userids

resp_logger = logging.getLogger(__name__)


def __log_resptime(timer, action_message):
    resp_logger.info(
        {**action_message,
         **{'Time': "{} seconds".format(timer.get_elapsed())}})


def log_page_view(timer, request, template_name):
    msg = {'page': template_name,
           'session_key': hash_session_key(request)}
    if timer:
        __log_resptime(timer, msg)
    else:
        resp_logger.info(msg)


def log_api_call(timer, request, message):
    __log_resptime(timer,
                   {'api': message,
                    'session_key': hash_session_key(request)})


def log_client_side_action(request, interaction_type):
    if interaction_type is not None:
        resp_logger.info({'client-side interaction': interaction_type,
                          'session_key': hash_session_key(request)})


def log_err(logger, timer, exc_info):
    """
    exc_info is a string containing
    the full stack trace, the exception type and value
    """
    logger.error(
        {**get_userids(),
         **{'err': exc_info.format_exc(chain=False).splitlines(),
            'Time': "{} seconds".format(timer.get_elapsed())}})


def log_exception(logger, action, exc_info):
    """
    exc_info is a string containing
    the full stack trace, the exception type and value
    """
    logger.error(
        {**get_userids(),
         **{'at': action,
            'err': exc_info.format_exc(chain=False).splitlines()}})


def log_info(logger, msg_dict):
    logger.info({**get_userids(), **msg_dict})


def log_data_not_found_response(logger, timer):
    log_msg(logger, timer, {'msg': 'Data not found'})


def log_invalid_netid_response(logger, timer):
    log_msg(logger, timer, {'msg': 'Invalid netid, abort'})


def log_invalid_regid_response(logger, timer):
    log_msg(logger, timer, {'msg': 'Invalid regid, abort'})


def log_msg(logger, timer, action_message):
    log_info(logger, {'msg': action_message,
                      'Time': "{} seconds".format(timer.get_elapsed())})
