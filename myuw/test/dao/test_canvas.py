from django.test import TestCase
from myuw.dao.canvas import (
    get_canvas_active_enrollments, set_section_canvas_course_urls,
    get_canvas_course_from_section,
    get_canvas_course_url, sws_section_label, get_viewable_course_sections)
from uw_sws.exceptions import InvalidCanvasIndependentStudyCourse
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
        section1 = schedule.sections[0]
        self.assertEquals(section1.section_label(),
                          "2013,spring,PHYS,121/A")
        self.assertEquals(section1.canvas_course_url,
                          'https://test.edu/courses/249652')

        section2 = schedule.sections[1]
        self.assertEquals(section2.section_label(),
                          "2013,spring,PHYS,121/AC")
        self.assertEquals(section2.canvas_course_url,
                          'https://test.edu/courses/249652')

        section3 = schedule.sections[2]
        self.assertEquals(section3.section_label(),
                          "2013,spring,PHYS,121/AQ")
        self.assertEquals(section3.canvas_course_url,
                          'https://test.edu/courses/249652')

        section8 = schedule.sections[7]
        self.assertEquals(section8.section_label(),
                          "2013,spring,ARCTIC,200/A")
        self.assertIsNone(section8.canvas_course_url)

        section = schedule.sections[3]
        self.assertEquals(section.section_label(), "2013,spring,TRAIN,100/A")
        self.assertIsNotNone(section.canvas_course_url)

        section = schedule.sections[4]
        self.assertEquals(section.section_label(), "2013,spring,TRAIN,101/A")
        self.assertIsNotNone(section.canvas_course_url)

        req = get_request_with_user("jeos",
                                    get_request_with_date("2013-10-01"))
        schedule = get_schedule_by_term(req, get_current_quarter(req))
        canvas_active_enrollments = get_canvas_active_enrollments(req)
        self.assertIsNotNone(req.canvas_act_enrollments)
        self.assertRaises(InvalidCanvasIndependentStudyCourse,
                          set_section_canvas_course_urls,
                          canvas_active_enrollments,
                          schedule, req)


    def test_get_canvas_course_url(self):
        person = Person()
        person.uwnetid = "javerage"
        person.regid = "00000000000000000000000000000001"
        sws_section = get_section_by_label('2013,spring,TRAIN,101/A')
        self.assertIsNotNone(get_canvas_course_from_section(sws_section))
        self.assertEquals(get_canvas_course_url(sws_section, person),
                          'https://canvas.uw.edu/courses/149651')

    def test_sws_section_label(self):
        self.assertEquals(sws_section_label(None), (None, None))
        self.assertEquals(sws_section_label('course_12345'), (None, None))
        self.assertEquals(
            sws_section_label('2013-spring-TRAIN-100-A'),
            ('2013,spring,TRAIN,100/A', None))
        self.assertEquals(
            sws_section_label(
                '2013-spring-TRAIN-100-A-12345678901234567890123456789012'),
            ('2013,spring,TRAIN,100/A', '12345678901234567890123456789012'))
        self.assertEquals(
            sws_section_label('2013-spring-TRAIN-100-AB'),
            ('2013,spring,TRAIN,100/AB', None))
        self.assertEquals(
            sws_section_label('2013-spring-TRAIN-100-A--'),
            ('2013,spring,TRAIN,100/A', None))
        self.assertEquals(
            sws_section_label(
                '2013-spring-TRAIN-100-A-12345678901234567890123456789012--'),
            ('2013,spring,TRAIN,100/A', '12345678901234567890123456789012'))
