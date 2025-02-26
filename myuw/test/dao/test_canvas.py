# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from restclients_core.exceptions import DataFailureException
from myuw.dao.canvas import (
    get_canvas_active_enrollments, set_section_canvas_course_urls,
    get_canvas_course_from_section,
    get_canvas_course_url, sws_section_label, get_viewable_course_sections)
from uw_sws.models import Person
from uw_sws.section import get_section_by_label
from myuw.dao.term import get_current_quarter
from myuw.dao.registration import get_schedule_by_term
from myuw.test import (
    fdao_sws_override, get_request_with_user, get_request,
    get_request_with_date)


@fdao_sws_override
class TestCanvas(TestCase):
    def setUp(self):
        get_request()

    def test_get_canvas_active_enrollments(self):
        req = get_request_with_user("eight")
        schedule = get_schedule_by_term(req, get_current_quarter(req))

        canvas_active_enrollments = get_canvas_active_enrollments(req)
        self.assertIsNotNone(req.canvas_act_enrollments)

        set_section_canvas_course_urls(canvas_active_enrollments,
                                       schedule, req)
        section1 = schedule.sections[2]
        self.assertEqual(section1.section_label(),
                         "2013,spring,PHYS,121/AQ")
        self.assertEqual(section1.canvas_course_url,
                         'https://test.edu/courses/249652')

        section2 = schedule.sections[1]
        self.assertEqual(section2.section_label(),
                         "2013,spring,PHYS,121/AC")
        self.assertEqual(section2.canvas_course_url,
                         'https://test.edu/courses/249652')

        section3 = schedule.sections[2]
        self.assertEqual(section3.section_label(),
                         "2013,spring,PHYS,121/AQ")
        self.assertEqual(section3.canvas_course_url,
                         'https://test.edu/courses/249652')

        section8 = schedule.sections[7]
        self.assertEqual(section8.section_label(),
                         "2013,spring,ARCTIC,200/A")
        self.assertIsNone(section8.canvas_course_url)

        section = schedule.sections[3]
        self.assertEqual(section.section_label(), "2013,spring,TRAIN,100/A")
        self.assertIsNotNone(section.canvas_course_url)

        section = schedule.sections[4]
        self.assertEqual(section.section_label(), "2013,spring,TRAIN,101/A")
        self.assertIsNotNone(section.canvas_course_url)

        req = get_request_with_user("jbothell")
        schedule = get_schedule_by_term(req, get_current_quarter(req))
        self.assertRaises(
            DataFailureException, get_canvas_active_enrollments, req)

    def test_InvalidCanvasIndependentStudyCourse_case(self):
        req = get_request_with_user("jeos",
                                    get_request_with_date("2013-10-01"))
        schedule = get_schedule_by_term(req, get_current_quarter(req))
        canvas_active_enrollments = get_canvas_active_enrollments(req)
        self.assertIsNotNone(req.canvas_act_enrollments)
        set_section_canvas_course_urls(canvas_active_enrollments,
                                       schedule, req)
        # InvalidCanvasIndependentStudyCourse
        self.assertIsNone(schedule.sections[0].canvas_course_url)

    def test_get_canvas_course_url(self):
        person = Person()
        person.uwnetid = "javerage"
        person.regid = "00000000000000000000000000000001"
        sws_section = get_section_by_label('2013,spring,TRAIN,101/A')
        self.assertIsNotNone(get_canvas_course_from_section(sws_section))
        self.assertEqual(get_canvas_course_url(sws_section, person),
                         'https://canvas.uw.edu/courses/149651')

    def test_sws_section_label(self):
        self.assertEqual(sws_section_label(None), (None, None))
        self.assertEqual(sws_section_label('course_12345'), (None, None))
        self.assertEqual(
            sws_section_label('2013-spring-TRAIN-100-A'),
            ('2013,spring,TRAIN,100/A', None))
        self.assertEqual(
            sws_section_label(
                '2013-spring-TRAIN-100-A-12345678901234567890123456789012'),
            ('2013,spring,TRAIN,100/A', '12345678901234567890123456789012'))
        self.assertEqual(
            sws_section_label('2013-spring-TRAIN-100-AB'),
            ('2013,spring,TRAIN,100/AB', None))
        self.assertEqual(
            sws_section_label('2013-spring-TRAIN-100-A--'),
            ('2013,spring,TRAIN,100/A', None))
        self.assertEqual(
            sws_section_label(
                '2013-spring-TRAIN-100-A-12345678901234567890123456789012--'),
            ('2013,spring,TRAIN,100/A', '12345678901234567890123456789012'))
