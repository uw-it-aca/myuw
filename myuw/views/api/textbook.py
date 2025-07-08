# Copyright 2025 UW-IT, University of Washington
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
    get_sln_textbook_json, get_order_url, get_iacourse_status)
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_api_call
from myuw.views import prefetch_resources
from myuw.views.api import ProtectedAPI
from myuw.views.error import handle_exception, data_not_found

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
            sln_books = {}
            stud_course_slns = set()
            inst_course_slns = set()
            try:
                # student enrolled sections
                schedule = get_schedule_by_term(
                    request, term=term, summer_term=summer_term)
                stud_course_slns = _get_sln_set(schedule)
                logger.debug(f"Student SLNs: {stud_course_slns}")

                if stud_course_slns:
                    sln_books["order_url"] = get_order_url(
                        term.quarter, stud_course_slns)
            except DataFailureException as ex:
                if ex.status != 400 and ex.status != 404:
                    raise

            try:
                # inst sections (not split summer terms)
                schedule = get_instructor_schedule_by_term(
                    request, term=term, summer_term="full-term")
                inst_course_slns = _get_sln_set(schedule)
                logger.debug(f"Instructor SLNs: {inst_course_slns}")
            except DataFailureException as ex:
                if ex.status != 404:
                    raise

            sln_set = stud_course_slns | inst_course_slns
            if sln_set:
                try:
                    sln_books.update(
                        get_sln_textbook_json(term.quarter, sln_set))
                except DataFailureException as ex:
                    if ex.status != 400 and ex.status != 404:
                        raise
            logger.debug(
                f"Get Textbook for {term.year}.{term.quarter} {sln_books}")
            log_api_call(
                timer, request,
                f"Get Textbook for {term.year}.{term.quarter}")
            return self.json_response(sln_books)

        except Exception:
            return handle_exception(logger, timer, traceback)


def _get_sln_set(schedule):
    return {
        section.sln
        for section in schedule.sections
        if not section.is_campus_tacoma() and section.sln
    }


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
            if ret_obj is None:
                return data_not_found()
            return self.json_response(ret_obj.json_data())
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
            if ret_obj is None:
                return data_not_found()
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
