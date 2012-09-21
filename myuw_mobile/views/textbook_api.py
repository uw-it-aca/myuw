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
from rest_dispatch import RESTDispatch
from pws_util import is_valid_netid
from page import get_netid_from_session


class TextbookCurQuar(RESTDispatch):
    """
    Performs actions on resource at /api/v1/books/current/.
    """
    _logger = logging.getLogger('myuw_mobile.views.textbook_api.TextbookCurQuar')

    def GET(self, request):
        """
        GET returns 200 with textbooks for the current quarter
        """

        netid = get_netid_from_session(request);
        if not netid or not is_valid_netid(netid):
            return super(TextbookCurQuar, 
                         self).invalid_session(*args, **named_args)

        schedule_dao = ScheduleDao(netid)
        schedule = schedule_dao.get_cur_quarter_schedule()

        books_dao = Bookstore()
        try:
            book_data = books_dao.get_books_for_schedule(schedule)
        except Exception, message:
            print netid + ' failed to get textbook list: ', message
            traceback.print_exc(file=sys.stdout)
            return super(TextbookCurQuar,
                         self).data_not_found(*args, **named_args)

        if not book_data:
            return super(TextbookCurQuar,
                         self).data_not_found(*args, **named_args)

        response = HttpResponse(get_json(book_data))
        response.status_code = 200
        return response


def get_json(book_data):
    json_data = {}
    for sln in book_data:
        json_data[sln] = []
        for book in book_data[sln]:
            json_data[sln].append(book.json_data())
    return json.dumps(json_data)

