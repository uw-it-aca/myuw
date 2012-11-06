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
from myuw_mobile.dao.textbook import Textbook
from rest_dispatch import RESTDispatch, data_not_found
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logresp import log_data_not_found_response, log_success_response

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
        schedule = ScheduleDao().get_cur_quarter_schedule()
        if not schedule:
            log_data_not_found_response(logger, timer)
            return data_not_found()

        book_data = Textbook().get(schedule)
        if not book_data:
            log_data_not_found_response(logger, timer)
            return data_not_found()

        verba_link = Textbook().get_verba_link(schedule)

        log_success_response(logger, timer)

        by_sln = index_by_sln(book_data)
        by_sln["verba_link"] = verba_link
        return HttpResponse(json.dumps(by_sln))


def index_by_sln(book_data):
    json_data = {}
    for sln in book_data:
        json_data[sln] = []
        for book in book_data[sln]:
            json_data[sln].append(book.json_data())
    return json_data

