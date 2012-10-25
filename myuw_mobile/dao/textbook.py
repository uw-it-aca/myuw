from django.conf import settings
import logging
import traceback
from myuw_mobile.dao.sws import Schedule
from restclients.bookstore import Bookstore
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logback import log_resp_time, log_exception

class Textbook():
    """
    encapsulates the interactions with the Bookstore web service.
    """
    _logger = logging.getLogger('myuw_mobile.dao.textbook.Textbook')

    def get(self, schedule):
        """
        returns textbooks for the schedule
        """
        timer = Timer()
        book_data = None
        try:
            book_data = Bookstore().get_books_for_schedule(schedule)
        except Exception as ex:
            log_exception(Textbook._logger, 
                         'get_books_for_schedule', 
                          traceback.format_exc(1))
        finally:
            log_resp_time(Textbook._logger,
                         'get_books_for_schedule',
                          timer)

        return book_data

