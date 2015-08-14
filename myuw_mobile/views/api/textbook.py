import logging
from django.http import HttpResponse
import json
from myuw_mobile.dao.schedule import get_schedule_by_term
from myuw_mobile.dao.schedule import filter_schedule_sections_by_summer_term
from myuw_mobile.dao.term import get_specific_quarter, get_current_quarter
from myuw_mobile.dao.term.current import get_current_summer_term
from myuw_mobile.dao.textbook import get_textbook_by_schedule
from myuw_mobile.dao.textbook import get_verba_link_by_schedule
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logresp import log_data_not_found_response
from myuw_mobile.logger.logresp import log_success_response
from myuw_mobile.views.rest_dispatch import RESTDispatch, data_not_found


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
        logger = logging.getLogger(__name__)

        term = get_specific_quarter(year=year, quarter=quarter)
        schedule = get_schedule_by_term(term)
        if summer_term is not None:
            summer_term = summer_term.replace(",", "")
            filter_schedule_sections_by_summer_term(schedule, summer_term)

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
