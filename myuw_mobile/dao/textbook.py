"""
encapsulates the interactions with the Bookstore web service.
"""

import logging
import traceback
from django.conf import settings
from restclients.bookstore import Bookstore
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logback import log_resp_time, log_exception


logger = logging.getLogger(__name__)


def get_textbook_by_schedule(schedule):
    """
    returns textbooks for the schedule
    """
    timer = Timer()
    book_data = None
    try:
        book_data = Bookstore().get_books_for_schedule(schedule)
    except Exception as ex:
        log_exception(logger, 
                     'get_books_for_schedule', 
                      traceback.format_exc())
    finally:
        log_resp_time(logger,
                     'get_books_for_schedule',
                      timer)

    return book_data


def get_verba_link_by_schedule(schedule):
    """
    returns a link to the verba price compare page for a schedule
    """
    timer = Timer()
    verba_link = None
    try:
        verba_link = Bookstore().get_verba_link_for_schedule(schedule)
    except Exception as ex:
        log_exception(logger,
                     'get_verba_link',
                      traceback.format_exc())
    finally:
        log_resp_time(logger,
                     'get_verba_link',
                      timer)

    return verba_link

