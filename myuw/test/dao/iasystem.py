# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import datetime
import pytz
from django.test import TestCase
from django.conf import settings
from django.test.utils import override_settings
from uw_sws.models import Section
from uw_iasystem.evaluation import get_evaluation_by_id
from uw_sws.section import get_section_by_label
from myuw.dao.iasystem import json_for_evaluation, _get_evaluations_domain,\
    _get_evaluations_by_section_and_student, summer_term_overlaped,\
    get_evaluation_by_section_and_instructor
from myuw.dao.registration import get_schedule_by_term
from myuw.dao.term import get_current_quarter
from myuw.test import fdao_pws_override, fdao_sws_override, fdao_ias_override,\
    get_request_with_date, get_request_with_user, get_request


@fdao_ias_override
@fdao_pws_override
@fdao_sws_override
class IASystemDaoTest(TestCase):
    def setUp(self):
        get_request()

    def test_get_evaluations_domain(self):
        section = get_section_by_label('2013,spring,AAES,150/A')
        self.assertEqual(_get_evaluations_domain(section), 'PCE_IELP')

        section = get_section_by_label('2013,spring,BIGDATA,230/A')
        self.assertEqual(_get_evaluations_domain(section), "PCE_OL")

        section = get_section_by_label('2013,winter,PSYCH,203/A')
        self.assertEqual(_get_evaluations_domain(section), "PCE_OL")

        section = get_section_by_label('2013,spring,ACCTG,508/A')
        self.assertEqual(_get_evaluations_domain(section), "Seattle")

    def test_summer_term_overlaped(self):
        section = Section()
        section.summer_term = "A-term"
        now_request = get_request_with_user(
            'javerage', get_request_with_date("2013-07-10"))
        term = get_current_quarter(now_request)
        section.term = term
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
        req = get_request_with_user('javerage',
                                    get_request_with_date("2013-07-01"))
        term = get_current_quarter(req)
        section = Section()
        section.summer_term = "A-term"
        section.term = term
        schedule = get_schedule_by_term(req, term)
        evals = None
        for section in schedule.sections:
            if section.curriculum_abbr == 'ELCBUS':
                evals = _get_evaluations_by_section_and_student(section,
                                                                1443336)
                break
        self.assertIsNotNone(evals)
        self.assertEqual(evals[0].section_sln, 13833)
        self.assertEqual(evals[0].eval_open_date,
                         datetime.datetime(2013, 7, 2,
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
                         "2013-07-23 06:59:59+00:00")
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
                         "2013-03-23 07:59:59+00:00")

        now_request = get_request_with_date("2013-03-22")
        json_data = json_for_evaluation(now_request, evals, None)
        self.assertIsNotNone(json_data)
        self.assertEqual(len(json_data), 1)
        self.assertEqual(json_data[0]['instructors'][0]['instructor_title'],
                         u'Teaching Assistant')
        self.assertEqual(json_data[0]['close_date'],
                         "2013-03-23 07:59:59+00:00")
        # after close date
        now_request = get_request_with_date("2013-03-24")
        json_data = json_for_evaluation(now_request, evals, None)
        self.assertEqual(len(json_data), 0)

    def test_multiple_instructors(self):
        req = get_request_with_user('javerage',
                                    get_request_with_date("2013-08-01"))
        term = get_current_quarter(req)
        schedule = get_schedule_by_term(req, term)
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
        self.assertTrue(evals[0].is_seattle)
        self.assertEqual(len(evals[0].instructor_ids), 3)
        self.assertEqual(evals[0].instructor_ids[0], 123456781)
        self.assertEqual(evals[0].instructor_ids[1], 123456782)
        self.assertEqual(evals[0].instructor_ids[2], 123456798)

    def test_multiple_evals(self):
        req = get_request_with_user('javerage',
                                    get_request_with_date("2013-04-01"))
        term = get_current_quarter(req)
        schedule = get_schedule_by_term(req, term)
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
        self.assertFalse(evals[2].is_completed)
        now_request = get_request_with_date("2013-05-30")
        json_data = json_for_evaluation(now_request, evals, None)
        self.assertEqual(len(json_data), 0)

        # open dates of 1 eval
        now_request = get_request_with_date("2013-05-31")
        json_data = json_for_evaluation(now_request, evals, None)
        self.assertIsNotNone(json_data)
        self.assertEqual(len(json_data), 1)
        self.assertEqual(json_data[0]['close_date'],
                         "2013-07-01 07:59:59+00:00")
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
                         "2013-07-01 07:59:59+00:00")
        self.assertEqual(json_data[1]['close_date'],
                         "2013-06-17 06:59:59+00:00")

        # after open dates of three evals
        now_request = get_request_with_date("2013-06-10")
        json_data = json_for_evaluation(now_request, evals, None)
        self.assertIsNotNone(json_data)
        self.assertEqual(len(json_data), 3)

        # after close date of one eval
        now_request = get_request_with_date("2013-06-17")
        json_data = json_for_evaluation(now_request, evals, None)
        self.assertEqual(len(json_data), 2)
        self.assertEqual(json_data[0]['close_date'],
                         "2013-07-01 07:59:59+00:00")

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

    def test_pce_instructor_evals(self):
        section = get_section_by_label('2013,spring,AAES,150/A')
        instructor_id = "100000011"
        evals = get_evaluation_by_section_and_instructor(
            section, instructor_id)
        self.assertIsNotNone(evals)
        self.assertEqual(len(evals), 1)
        self.assertEqual(evals[0].section_sln, 164406)
        self.assertEqual(evals[0].domain, "uweo-ielp")
        self.assertTrue(evals[0].is_eo_ielp)

        section = get_section_by_label('2013,spring,BIGDATA,230/A')
        evals = get_evaluation_by_section_and_instructor(
            section, instructor_id)
        self.assertIsNotNone(evals)
        self.assertEqual(len(evals), 1)
        self.assertEqual(evals[0].section_sln, 157956)
        self.assertEqual(evals[0].domain, "uweo-ap")
        self.assertTrue(evals[0].is_eo_ap)

        section = get_section_by_label('2013,spring,CPROGRM,712/A')
        evals = get_evaluation_by_section_and_instructor(
            section, instructor_id)
        self.assertIsNotNone(evals)
        self.assertEqual(len(evals), 1)
        self.assertEqual(evals[0].section_sln, 157462)
        self.assertEqual(evals[0].domain, "uweo-ap")

    def test_pce_student_evals(self):
        section = get_section_by_label('2013,spring,BIGDATA,230/A')
        student_id = "1000055"
        evals = _get_evaluations_by_section_and_student(section, student_id)
        self.assertIsNotNone(evals)
        self.assertEqual(len(evals), 1)
        self.assertFalse(evals[0].is_closed())
        self.assertFalse(evals[0].is_completed)
