from myuw.dao import get_netid_of_original_user, get_netid_of_current_user


def log_exception(logger, action, exc_info):
    """
    exc_info is a string containing
    the full stack trace, the exception type and value
    """
    logger.error("{} - {} => {} ".format(get_logging_userid(),
                                         action,
                                         exc_info.splitlines()))


def log_exception_with_timer(logger, timer, exc_info):
    logger.error("{} - {} Time={} seconds".format(get_logging_userid(),
                                                  exc_info.splitlines(),
                                                  timer.get_elapsed()))


def log_info(logger, message):
    logger.info("{} {}".format(get_logging_userid(),
                               message))


def log_time(logger, action_message, timer):
    log_info(logger,
             "{}. Time={} seconds".format(action_message,
                                          timer.get_elapsed()))


def get_logging_userid():
    """
    Return <actual user netid> acting_as: <override user netid> if
    the user is acting as someone else, otherwise
    <actual user netid> no_override: <actual user netid>
    """
    override_userid = get_netid_of_current_user()
    actual_userid = get_netid_of_original_user()
    log_format = 'base_user: {} acting_user: {} is_override: {}. '
    try:
        if override_userid != actual_userid:
            log_userid = log_format.format(actual_userid,
                                           override_userid,
                                           'true')
        else:
            log_userid = log_format.format(actual_userid,
                                           actual_userid,
                                           'false')
    except TypeError:
        return None
    return log_userid
