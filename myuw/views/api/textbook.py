import json
import logging
import traceback
from django.http import HttpResponse
from myuw.dao.gws import is_student
from myuw.dao.schedule import get_schedule_by_term
from myuw.dao.schedule import filter_schedule_sections_by_summer_term
from myuw.dao.term import get_specific_term, get_current_quarter,\
    get_current_summer_term
from myuw.dao.textbook import get_textbook_by_schedule
from myuw.dao.textbook import get_verba_link_by_schedule
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_success_response, log_msg, log_err
from myuw.views.rest_dispatch import RESTDispatch, data_error, data_not_found


logger = logging.getLogger(__name__)


class Textbook(RESTDispatch):
    """
    Performs actions on resource at /api/v1/books/current/.
    """

    def GET(self, request, year, quarter, summer_term):
        """
        GET returns 200 with textbooks for the current quarter
        """
        return self.respond(year, quarter, summer_term)

    def respond(self, year, quarter, summer_term):
        timer = Timer()
        try:
            if not is_student():
                log_msg(logger, timer, "Not a student, abort!")
                return data_not_found()

            term = get_specific_term(year=year, quarter=quarter)
            schedule = get_schedule_by_term(term)
            if summer_term is not None and len(summer_term) > 0:
                summer_term = summer_term.replace(",", "")
                filter_schedule_sections_by_summer_term(schedule, summer_term)

            book_data = get_textbook_by_schedule(schedule)

            verba_link = get_verba_link_by_schedule(schedule)

            by_sln = index_by_sln(book_data)
            by_sln["verba_link"] = verba_link
            log_success_response(logger, timer)
            return HttpResponse(json.dumps(by_sln))
        except Exception:
            log_err(logger, timer, traceback.format_exc())
            return data_error()


def index_by_sln(book_data):
    json_data = {}
    for sln in book_data:
        json_data[sln] = []
        for book in book_data[sln]:
            json_data[sln].append(book.json_data())
    return json_data


class TextbookCur(Textbook):
    """
    Performs actions on resource at /api/v1/schedule/current/.
    """

    def GET(self, request):
        """
        GET returns 200 with the current quarter Textbook
        """
        term = get_current_quarter(request)
        summer_term = ""
        if term.quarter == "summer":
            summer_term = get_current_summer_term(request)
        return self.respond(term.year, term.quarter, summer_term)
