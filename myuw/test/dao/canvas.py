from django.test import TestCase
from myuw.dao.canvas import _get_canvas_enrollment_dict_for_regid
from myuw.dao.schedule import _get_schedule
from myuw.dao.term import get_current_quarter
from myuw.test import fdao_sws_override, get_request_with_user, get_request


@fdao_sws_override
class TestCanvas(TestCase):
    def setUp(self):
        get_request()

    def test_crosslinks(self):
        data = _get_canvas_enrollment_dict_for_regid(
            "12345678901234567890123456789012")

        physics = data['2013,spring,PHYS,121/A']
        self.assertEquals(physics.course_url,
                          'https://canvas.uw.edu/courses/249652')

        has_section_b = '2013,spring,TRAIN,100/B' in data
        self.assertTrue(has_section_b)

        has_section_a = '2013,spring,TRAIN,100/A' in data
        self.assertTrue(has_section_a)

        train = data['2013,spring,TRAIN,100/A']
        self.assertEquals(train.course_url,
                          'https://canvas.uw.edu/courses/249650')
        self.assertFalse(physics.is_unpublished())
