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
from myuw_mobile.dao.pws import Person as PersonDao
from myuw_mobile.user import UserService


class TextbookCurQuar(RESTDispatch):
    """
    Performs actions on resource at /api/v1/books/current/.
    """
    _logger = logging.getLogger('myuw_mobile.views.textbook_api.TextbookCurQuar')

    def GET(self, request):
        """
        GET returns 200 with textbooks for the current quarter
        """

        user_service = UserService(request)
        schedule_dao = ScheduleDao(user_service)
        schedule = schedule_dao.get_cur_quarter_schedule()
        if not schedule:
            return data_not_found()

        books_dao = Bookstore()
        try:
            book_data = books_dao.get_books_for_schedule(schedule)
        except Exception, message:
            print netid + ' failed to get textbook list: ', message
            traceback.print_exc(file=sys.stdout)

        if not book_data:
            return data_not_found()

        return HttpResponse(index_by_sln(book_data))


def index_by_sln(book_data):
    json_data = {}
    for sln in book_data:
        json_data[sln] = []
        for book in book_data[sln]:
            json_data[sln].append(book.json_data())
    return json.dumps(json_data)

