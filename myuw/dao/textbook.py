"""
encapsulates the interactions with the Bookstore web service.
"""

import logging
from restclients.bookstore import Bookstore
from myuw.logger.timer import Timer
from myuw.logger.logback import log_resp_time


logger = logging.getLogger(__name__)


def get_textbook_by_schedule(schedule):
    """
    returns textbooks for a valid schedule
    """
    timer = Timer()
    try:
        return Bookstore().get_books_for_schedule(schedule)
    finally:
        log_resp_time(logger,
                      'get_books_for_schedule',
                      timer)


def get_verba_link_by_schedule(schedule):
    """
    returns a link to the verba price compare page for a valid schedule
    """
    timer = Timer()
    try:
        return Bookstore().get_verba_link_for_schedule(schedule)
    finally:
        log_resp_time(logger,
                      'get_verba_link',
                      timer)
