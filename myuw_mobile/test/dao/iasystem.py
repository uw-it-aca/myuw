import datetime
import pytz
from django.test import TestCase
from django.conf import settings
from django.test.client import RequestFactory
from restclients.models.sws import Term, Section
from restclients.iasystem.evaluation import get_evaluation_by_id
from myuw_mobile.dao.iasystem import json_for_evaluation,\
    _get_evaluations_by_section_and_student
from myuw_mobile.dao.schedule import _get_schedule


class IASystemTest(TestCase):

    def test_get_evaluations_by_section(self):
        with self.settings(
            RESTCLIENTS_IASYSTEM_DAO_CLASS=\
                'restclients.dao_implementation.iasystem.File',
            RESTCLIENTS_PWS_DAO_CLASS=\
                'restclients.dao_implementation.pws.File',
            RESTCLIENTS_SWS_DAO_CLASS=\
                'restclients.dao_implementation.sws.File'):

            regid = "9136CCB8F66711D5BE060004AC494FFE"
            term = Term()
            term.year = 2013
            term.quarter = "summer"
            schedule = _get_schedule(regid, term)
            evals = None
            for section in schedule.sections:
                if section.curriculum_abbr == 'ELCBUS':
                    evals = _get_evaluations_by_section_and_student(section,
                                                                    1443336)
                    break
            self.assertEqual(evals[0].section_sln, 13833)
            self.assertEqual(evals[0].eval_open_date,
                             datetime.datetime(2013, 07, 02,
                                               14, 0,
                                               tzinfo=pytz.utc))
            self.assertEqual(evals[0].eval_close_date,
                             datetime.datetime(2013, 07, 23,
                                               6, 59, 59,
                                               tzinfo=pytz.utc))
            now_request = RequestFactory().get("/")
            # after open date, before show date
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-07-16"
            json_data = json_for_evaluation(now_request, evals, "A-term")
            self.assertIsNone(json_data['close_date'])
            # after show date
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-07-17"
            json_data = json_for_evaluation(now_request, evals, "A-term")
            self.assertIsNotNone(json_data['close_date'])
            # before close date
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-07-22"
            json_data = json_for_evaluation(now_request, evals, "A-term")
            self.assertIsNotNone(json_data['close_date'])
            # before hide date but after close date
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-07-24"
            json_data = json_for_evaluation(now_request, evals, "A-term")
            self.assertIsNone(json_data['close_date'])

    def test_json_for_evaluation(self):
        with self.settings(
            RESTCLIENTS_IASYSTEM_DAO_CLASS=\
                'restclients.dao_implementation.iasystem.File',
            RESTCLIENTS_PWS_DAO_CLASS=\
                'restclients.dao_implementation.pws.File',
            RESTCLIENTS_SWS_DAO_CLASS=\
                'restclients.dao_implementation.sws.File'):

            evals = get_evaluation_by_id(132136, "seattle")
            now_request = RequestFactory().get("/")
            # after show date, before open date
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-03-11"
            json_data = json_for_evaluation(now_request, evals, None)
            self.assertIsNone(json_data['close_date'])
            # after open date
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-03-13"
            json_data = json_for_evaluation(now_request, evals, None)
            self.assertIsNotNone(json_data['close_date'])

            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-03-22"
            json_data = json_for_evaluation(now_request, evals, None)
            self.assertIsNotNone(json_data['close_date'])
            # before hide date but after close date
            now_request.session = {}
            now_request.session["myuw_override_date"] = "2013-03-24"
            json_data = json_for_evaluation(now_request, evals, None)
            self.assertIsNone(json_data['close_date'])
