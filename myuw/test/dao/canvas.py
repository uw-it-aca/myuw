from django.test import TestCase
<<<<<<< HEAD
=======
from django.test.client import RequestFactory
from userservice.user import UserServiceMiddleware
>>>>>>> dcf0d3a63c30e729c8e6b43e20f4d26c08b01079
from myuw.dao.canvas import _get_canvas_enrollment_dict_for_regid
from myuw.dao.schedule import _get_schedule
from myuw.dao.term import get_current_quarter
from myuw.test import fdao_sws_override, get_request_with_user, get_request


@fdao_sws_override
class TestCanvas(TestCase):
    def setUp(self):
        get_request()

    def test_crosslinks(self):
<<<<<<< HEAD
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
=======
        with self.settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS):

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
>>>>>>> dcf0d3a63c30e729c8e6b43e20f4d26c08b01079
