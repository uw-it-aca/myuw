import logging
from django.http import HttpResponse
from django.utils import simplejson as json
from myuw_mobile.dao.schedule import get_current_quarter_schedule
from myuw_mobile.dao.textbook import get_textbook_by_schedule, get_verba_link_by_schedule
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logresp import log_data_not_found_response, log_success_response
from myuw_mobile.views.rest_dispatch import RESTDispatch, data_not_found


class TextbookCurQuar(RESTDispatch):
    """
    Performs actions on resource at /api/v1/books/current/.
    """

    def GET(self, request):
        """
        GET returns 200 with textbooks for the current quarter
        """
        timer = Timer()
        logger = logging.getLogger(__name__)
        schedule = get_current_quarter_schedule()
        if schedule is None:
            log_data_not_found_response(logger, timer)
            return data_not_found()

        book_data = get_textbook_by_schedule(schedule)
        if book_data is None:
            log_data_not_found_response(logger, timer)
            return data_not_found()

        verba_link = get_verba_link_by_schedule(schedule)

        by_sln = index_by_sln(book_data)
        by_sln["verba_link"] = verba_link
        log_success_response(logger, timer)
        return HttpResponse(json.dumps(by_sln))


def index_by_sln(book_data):
    json_data = {}
    for sln in book_data:
        json_data[sln] = []
        for book in book_data[sln]:
            json_data[sln].append(book.json_data())
    return json_data

