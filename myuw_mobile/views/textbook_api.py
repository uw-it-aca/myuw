from django.http import HttpResponse
from django.conf import settings
#from django.contrib import auth
#from django.contrib.auth.decorators import login_required
#from django.core.context_processors import csrf
#from django.views.decorators.csrf import csrf_protect
from django.utils import simplejson as json
import sys
import traceback
import logging
from myuw_mobile.dao.sws import Schedule as ScheduleDao
from restclients.bookstore import Bookstore
from rest_dispatch import RESTDispatch, data_not_found
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.util import log_data_not_found_response, log_success_response, log_exception, log_resp_time

class TextbookCurQuar(RESTDispatch):
    """
    Performs actions on resource at /api/v1/books/current/.
    """

    def GET(self, request):
        """
        GET returns 200 with textbooks for the current quarter
        """
        timer = Timer()
        logger = logging.getLogger('myuw_mobile.views.textbook_api.TextbookCurQuar.GET')
        schedule_dao = ScheduleDao()
        schedule = schedule_dao.get_cur_quarter_schedule()
        if not schedule:
            log_data_not_found_response(logger, timer)
            return data_not_found()

        books_dao = Bookstore()
        book_data = None
        try:
            book_data = books_dao.get_books_for_schedule(schedule)
        except Exception, message:
            traceback.print_exc(file=sys.stdout)
            log_exception(logger, 
                         'books_dao.get_books_for_schedule', 
                          message)
        finally:
            log_resp_time(logger,
                         'books_dao.get_books_for_schedule',
                          timer)

        if not book_data:
            log_data_not_found_response(logger, timer)
            return data_not_found()

        log_success_response(logger, timer)
        return HttpResponse(index_by_sln(book_data))


def index_by_sln(book_data):
    json_data = {}
    for sln in book_data:
        json_data[sln] = []
        for book in book_data[sln]:
            json_data[sln].append(book.json_data())
    return json.dumps(json_data)

