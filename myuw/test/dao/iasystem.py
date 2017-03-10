import datetime
import pytz
from django.test import TestCase
from django.conf import settings
from django.test.utils import override_settings
from uw_sws.models import Section, Term
from restclients.iasystem.evaluation import get_evaluation_by_id
from myuw.dao.iasystem import json_for_evaluation,\
    _get_evaluations_by_section_and_student, summer_term_overlaped
from myuw.dao.schedule import _get_schedule
from myuw.test import fdao_pws_override, fdao_sws_override,\
    get_request_with_date, get_request_with_user, get_request


FDAO_IAS = 'restclients.dao_implementation.iasystem.File'
fdao_ias_override = override_settings(
    RESTCLIENTS_IASYSTEM_DAO_CLASS=FDAO_IAS
)


@fdao_ias_override
@fdao_pws_override
@fdao_sws_override
class IASystemDaoTest(TestCase):
    def setUp(self):
        get_request()

    def test_summer_term_overlaped(self):
        term = Term()
        term.year = 2013
        term.quarter = "summer"
        section = Section()
        section.summer_term = "A-term"
        section.term = term

        now_request = get_request_with_date("2013-07-10")
        self.assertTrue(summer_term_overlaped(now_request, section))
        section.summer_term = "Full-term"
        self.assertFalse(summer_term_overlaped(now_request, section))
        now_request = get_request_with_date("2013-08-10")
        self.assertTrue(summer_term_overlaped(now_request, section))

        section.summer_term = "B-term"
        self.assertTrue(summer_term_overlaped(now_request, section))

        now_request = get_request_with_date("2013-03-10")
        self.assertTrue(summer_term_overlaped(now_request, 'None'))
        self.assertTrue(summer_term_overlaped(now_request, '-'))

    def test_get_evaluations_by_section(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        term = Term()
        term.year = 2013
        term.quarter = "summer"
        section = Section()
        section.summer_term = "A-term"
        section.term = term
        schedule = _get_schedule(regid, term)
        evals = None
        for section in schedule.sections:
            if section.curriculum_abbr == 'ELCBUS':
                evals = _get_evaluations_by_section_and_student(section,
                                                                1443336)
                break
        self.assertIsNotNone(evals)
        self.assertEqual(evals[0].section_sln, 13833)
        self.assertEqual(evals[0].eval_open_date,
                         datetime.datetime(2013, 7, 02,
                                           14, 0,
                                           tzinfo=pytz.utc))
        self.assertEqual(evals[0].eval_close_date,
                         datetime.datetime(2013, 7, 23,
                                           6, 59, 59,
                                           tzinfo=pytz.utc))
        self.assertFalse(evals[0].is_completed)

        now_request = get_request()

        # after open date
        now_request = get_request_with_date("2013-07-03")
        json_data = json_for_evaluation(now_request, evals, section)
        self.assertIsNotNone(json_data)
        self.assertEqual(len(json_data), 1)
        self.assertEqual(json_data[0]['close_date'],
                         "2013-07-23 06:59:59 UTC+0000")
        # before close date
        now_request = get_request_with_date("2013-07-22")
        json_data = json_for_evaluation(now_request, evals, section)
        self.assertIsNotNone(json_data)
        self.assertEqual(len(json_data), 1)

        # after close date
        now_request = get_request_with_date("2013-07-24")
        json_data = json_for_evaluation(now_request, evals, section)
        self.assertEqual(len(json_data), 0)

    def test_json_for_evaluation(self):
        evals = get_evaluation_by_id(132136, "seattle")
        self.assertIsNotNone(evals)
        now_request = get_request_with_date("2013-03-11")
        # before open date
        json_data = json_for_evaluation(now_request, evals, None)
        self.assertEqual(len(json_data), 0)

        # after open date
        now_request = get_request_with_date("2013-03-13")
        json_data = json_for_evaluation(now_request, evals, None)
        self.assertIsNotNone(json_data)
        self.assertEqual(len(json_data), 1)
        self.assertEqual(json_data[0]['close_date'],
                         "2013-03-23 07:59:59 UTC+0000")

        now_request = get_request_with_date("2013-03-22")
        json_data = json_for_evaluation(now_request, evals, None)
        self.assertIsNotNone(json_data)
        self.assertEqual(len(json_data), 1)
        self.assertEqual(json_data[0]['close_date'],
                         "2013-03-23 07:59:59 UTC+0000")
        # after close date
        now_request = get_request_with_date("2013-03-24")
        json_data = json_for_evaluation(now_request, evals, None)
        self.assertEqual(len(json_data), 0)

    def test_multiple_instructors(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        term = Term()
        term.year = 2013
        term.quarter = "summer"
        schedule = _get_schedule(regid, term)
        evals = None
        for section in schedule.sections:
            if section.curriculum_abbr == 'TRAIN' and\
                    section.course_number == '102' and\
                    section.section_id == 'A':
                evals = _get_evaluations_by_section_and_student(section,
                                                                1033334)
                break
        self.assertIsNotNone(evals)
        self.assertEqual(len(evals), 1)
        self.assertEqual(evals[0].section_sln, 13833)
        self.assertEqual(evals[0].eval_open_date,
                         datetime.datetime(2013, 8, 23,
                                           14, 0, 0,
                                           tzinfo=pytz.utc))
        self.assertEqual(evals[0].eval_close_date,
                         datetime.datetime(2013, 8, 29,
                                           6, 59, 59,
                                           tzinfo=pytz.utc))

        self.assertEqual(len(evals[0].instructor_ids), 3)
        self.assertEqual(evals[0].instructor_ids[0], 123456781)
        self.assertEqual(evals[0].instructor_ids[1], 123456782)
        self.assertEqual(evals[0].instructor_ids[2], 123456798)

    def test_multiple_evals(self):
        regid = "9136CCB8F66711D5BE060004AC494FFE"
        term = Term()
        term.year = 2013
        term.quarter = "spring"
        schedule = _get_schedule(regid, term)
        evals = None
        for section in schedule.sections:
            if section.curriculum_abbr == 'TRAIN' and\
                    section.course_number == '100' and\
                    section.section_id == 'A':
                evals = _get_evaluations_by_section_and_student(section,
                                                                1033334)
                break
        self.assertIsNotNone(evals)
        self.assertEqual(len(evals), 3)
        self.assertEqual(evals[0].section_sln, 17169)
        self.assertEqual(evals[0].eval_open_date,
                         datetime.datetime(2013, 5, 30,
                                           15, 0, 0,
                                           tzinfo=pytz.utc))
        self.assertEqual(evals[0].eval_close_date,
                         datetime.datetime(2013, 7, 1,
                                           7, 59, 59,
                                           tzinfo=pytz.utc))
        self.assertFalse(evals[0].is_completed)
        self.assertEqual(evals[1].eval_open_date,
                         datetime.datetime(2013, 6, 5,
                                           7, 0, 0,
                                           tzinfo=pytz.utc))
        self.assertEqual(evals[1].eval_close_date,
                         datetime.datetime(2013, 6, 17,
                                           6, 59, 59,
                                           tzinfo=pytz.utc))
        self.assertFalse(evals[1].is_completed)
        self.assertEqual(evals[2].eval_open_date,
                         datetime.datetime(2013, 6, 10,
                                           7, 0, 0,
                                           tzinfo=pytz.utc))
        self.assertEqual(evals[2].eval_close_date,
                         datetime.datetime(2013, 6, 19,
                                           6, 59, 59,
                                           tzinfo=pytz.utc))
        self.assertTrue(evals[2].is_completed)
        now_request = get_request_with_date("2013-05-30")
        json_data = json_for_evaluation(now_request, evals, None)
        self.assertEqual(len(json_data), 0)

        # open dates of 1 eval
        now_request = get_request_with_date("2013-05-31")
        json_data = json_for_evaluation(now_request, evals, None)
        self.assertIsNotNone(json_data)
        self.assertEqual(len(json_data), 1)
        self.assertEqual(json_data[0]['close_date'],
                         "2013-07-01 07:59:59 UTC+0000")
        # after open dates of 1 eval
        now_request = get_request_with_date("2013-06-04")
        json_data = json_for_evaluation(now_request, evals, None)
        self.assertIsNotNone(json_data)
        self.assertEqual(len(json_data), 1)

        # after open dates of two evals
        now_request = get_request_with_date("2013-06-05")
        json_data = json_for_evaluation(now_request, evals, None)
        self.assertIsNotNone(json_data)
        self.assertEqual(len(json_data), 2)
        self.assertEqual(json_data[0]['close_date'],
                         "2013-07-01 07:59:59 UTC+0000")
        self.assertEqual(json_data[1]['close_date'],
                         "2013-06-17 06:59:59 UTC+0000")

        # after open dates of three evals
        now_request = get_request_with_date("2013-06-10")
        json_data = json_for_evaluation(now_request, evals, None)
        self.assertIsNotNone(json_data)
        self.assertEqual(len(json_data), 2)

        # after close date of one eval
        now_request = get_request_with_date("2013-06-17")
        json_data = json_for_evaluation(now_request, evals, None)
        self.assertEqual(len(json_data), 1)
        self.assertEqual(json_data[0]['close_date'],
                         "2013-07-01 07:59:59 UTC+0000")

        # after close date of two evals
        now_request = get_request_with_date("2013-06-19")
        json_data = json_for_evaluation(now_request, evals, None)
        self.assertEqual(len(json_data), 1)

        # after close date of last eval
        now_request = get_request_with_date("2013-07-02")
        json_data = json_for_evaluation(now_request, evals, None)
        self.assertEqual(len(json_data), 0)
        # for spring 2013, grade submission deadline is
        # the day after tomorrow!
