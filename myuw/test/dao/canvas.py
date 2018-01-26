from django.test import TestCase
from myuw.dao.canvas import (
    get_canvas_active_enrollments, canvas_course_is_available,
    get_canvas_course_from_section, get_canvas_course_url, sws_section_label,
    get_viewable_course_sections)
from uw_sws.models import Person
from uw_sws.section import get_section_by_label
from myuw.dao.term import get_current_quarter
from myuw.test import fdao_sws_override, get_request_with_user, get_request


@fdao_sws_override
class TestCanvas(TestCase):
    def setUp(self):
        get_request()

    def test_crosslinks(self):
        req = get_request_with_user("eight")
        self.assertFalse(hasattr(req, "canvas_act_enrollments"))
        data = get_canvas_active_enrollments(req)
        self.assertIsNotNone(req.canvas_act_enrollments)

        physics = data['2013,spring,PHYS,121/A']
        self.assertEquals(physics.course_url,
                          'https://canvas.uw.edu/courses/249652')

        self.assertTrue(canvas_course_is_available(physics.course_id))

        has_section_b = '2013,spring,TRAIN,100/B' in data
        self.assertTrue(has_section_b)

        has_section_a = '2013,spring,TRAIN,100/A' in data
        self.assertTrue(has_section_a)

        train = data['2013,spring,TRAIN,100/A']
        self.assertEquals(train.course_url,
                          'https://canvas.uw.edu/courses/249650')

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
