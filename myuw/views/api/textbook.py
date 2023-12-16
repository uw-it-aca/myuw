# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from datetime import timedelta
import logging
import traceback
from restclients_core.exceptions import DataFailureException
from myuw.dao.registration import get_schedule_by_term
from myuw.dao.instructor_schedule import get_instructor_schedule_by_term
from myuw.dao.term import (
  get_specific_term, get_comparison_date, get_current_quarter, get_term_after)
from myuw.dao.textbook import (
    get_textbook_by_schedule, get_order_url_by_schedule,
    get_iacourse_status)
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_api_call
from myuw.views import prefetch_resources
from myuw.views.api import ProtectedAPI
from myuw.views.error import handle_exception

logger = logging.getLogger(__name__)


class Textbook(ProtectedAPI):
    """
    Performs actions on resource at /api/v1/books/[year][quarter][summer_term].
    """
    def get(self, request, *args, **kwargs):
        """
        GET returns 200 with textbooks for the given quarter
        """
        timer = Timer()
        year = kwargs.get("year")
        quarter = kwargs.get("quarter")
        summer_term = kwargs.get("summer_term", "full-term")
        return self.respond(
            timer, request, get_specific_term(year, quarter), summer_term)

    def respond(self, timer, request, term, summer_term):
        try:
            prefetch_resources(request)
            by_sln = {}
            # enrolled sections
            try:
                schedule = get_schedule_by_term(
                    request, term=term, summer_term=summer_term)
                by_sln.update(_get_schedule_textbooks(schedule))

                order_url = get_order_url_by_schedule(schedule)
                if order_url:
                    by_sln["order_url"] = order_url
            except DataFailureException as ex:
                if ex.status != 400 and ex.status != 404:
                    raise

            # instructed sections (not split summer terms)
            try:
                schedule = get_instructor_schedule_by_term(
                    request, term=term, summer_term="full-term")
                by_sln.update(_get_schedule_textbooks(schedule))
            except DataFailureException as ex:
                if ex.status != 404:
                    raise

            # MUWM-5311: uwt no longer has books
            # if len(by_sln) == 0:
            #    log_data_not_found_response(logger, timer)
            #    return data_not_found()

            log_api_call(timer, request, "Get Textbook for {}.{}".format(
                term.year, term.quarter))
            return self.json_response(by_sln)

        except Exception:
            return handle_exception(logger, timer, traceback)


def _get_schedule_textbooks(schedule):
    by_sln = {}
    if schedule and len(schedule.sections):
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
            return self.respond(
                timer, request, get_current_quarter(request), None)
        except Exception:
            return handle_exception(logger, timer, traceback)


class IACDigitalItems(ProtectedAPI):
    # MUWM-5272

    def get(self, request, *args, **kwargs):
        """
        myuw_iacourse_digital_material_api
        GET returns 200 with textbooks for the given quarter
        """
        timer = Timer()
        year = kwargs.get("year")
        quarter = kwargs.get("quarter")
        try:
            ret_obj = get_iacourse_status(
                request, get_specific_term(year, quarter))
            if ret_obj:
                return self.json_response(ret_obj.json_data())
            return {}
        except Exception:
            return handle_exception(logger, timer, traceback)
        finally:
            log_api_call(
                timer, request, "IACourse_Status {}.{}".format(
                    year, quarter))


class IACDigitalItemsCur(ProtectedAPI):
    # MUWM-5272

    def get(self, request, *args, **kwargs):
        """
        myuw_iacourse_digital_material
        GET returns 200 with textbooks for the given quarter
        """
        timer = Timer()
        try:
            ret_obj = get_iacourse_status(
                request, get_payment_quarter(request))
            return self.json_response(ret_obj.json_data())
        except Exception:
            return handle_exception(logger, timer, traceback)
        finally:
            log_api_call(timer, request, "IACDigitalItemsCur")


def get_payment_quarter(request):
    term = get_current_quarter(request)
    term_after = get_term_after(term)
    comparison_date = get_comparison_date(request)
    if comparison_date > term_after.first_day_quarter - timedelta(days=6):
        return term_after
    return term
