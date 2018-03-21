import logging
import traceback
from restclients_core.exceptions import DataFailureException
from myuw.dao.schedule import (
    get_schedule_by_term, filter_schedule_sections_by_summer_term)
from myuw.dao.instructor_schedule import get_instructor_schedule_by_term
from myuw.dao.term import get_specific_term, get_current_quarter, \
    get_current_summer_term, get_comparison_datetime
from myuw.dao.textbook import get_textbook_by_schedule
from myuw.dao.textbook import get_order_url_by_schedule
from myuw.logger.timer import Timer
from myuw.logger.logresp import (
    log_success_response, log_msg, log_data_not_found_response)
from myuw.views import prefetch_resources
from myuw.views.api import ProtectedAPI
from myuw.views.error import handle_exception, data_not_found, data_error

logger = logging.getLogger(__name__)


class Textbook(ProtectedAPI):
    """
    Performs actions on resource at /api/v1/books/[year][quarter][summer_term].
    """
    def get(self, request, *args, **kwargs):
        """
        GET returns 200 with textbooks for the given quarter
        """
        current_date = get_comparison_datetime(request)
        year = kwargs.get("year")
        quarter = kwargs.get("quarter")
        summer_term = kwargs.get("summer_term")

        return self.respond(request, year, quarter, summer_term)

    def respond(self, request, year, quarter, summer_term):
        timer = Timer()
        try:
            prefetch_resources(request)
            by_sln = {}
            term = get_specific_term(year=year, quarter=quarter)
            # enrolled sections
            try:
                schedule = get_schedule_by_term(request, term)
                by_sln.update(self._get_schedule_textbooks(
                    schedule, summer_term))

                order_url = get_order_url_by_schedule(schedule)
                if order_url:
                    by_sln["order_url"] = order_url
                else:
                    raise DataFailureException("/api/v1/book/",
                                               404,
                                               "Unable to retrieve cart URL")
            except DataFailureException as ex:
                if ex.status != 400 and ex.status != 404:
                    raise

            # instructed sections
            try:
                schedule = get_instructor_schedule_by_term(request, term)
                by_sln.update(self._get_schedule_textbooks(
                    schedule, summer_term))
            except DataFailureException as ex:
                if ex.status != 404:
                    raise

            if len(by_sln) == 0:
                log_data_not_found_response(logger, timer)
                return data_not_found()

            log_success_response(logger, timer)
            return self.json_response(by_sln)
        except Exception:
            return handle_exception(logger, timer, traceback)

    def _get_schedule_textbooks(self, schedule, summer_term):
        by_sln = {}
        if schedule:
            if summer_term is not None and len(summer_term) > 0:
                summer_term = summer_term.replace(",", "")
                filter_schedule_sections_by_summer_term(
                    schedule, summer_term)

            if len(schedule.sections) > 0:
                book_data = get_textbook_by_schedule(schedule)
                by_sln.update(index_by_sln(book_data))

        return by_sln


def index_by_sln(book_data):
    json_data = {}
    for sln in book_data:
        json_data[sln] = []
        for book in book_data[sln]:
            json_data[sln].append(book.json_data())
    return json_data


class TextbookCur(Textbook):
    """
    Performs actions on resource at /api/v1/book/current/.
    """
    def get(self, request, *args, **kwargs):
        """
        GET returns 200 with the current quarter Textbook
        """
        timer = Timer()
        try:
            term = get_current_quarter(request)
            summer_term = ""
            if term.quarter == "summer":
                summer_term = get_current_summer_term(request)
            return self.respond(request, term.year,
                                term.quarter, summer_term)
        except Exception:
            return handle_exception(logger, timer, traceback)
