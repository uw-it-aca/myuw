from django.test import TestCase
from django.test.client import RequestFactory
from userservice.user import UserServiceMiddleware
from myuw.dao.canvas import _get_canvas_enrollment_dict_for_regid
from myuw.dao.schedule import _get_schedule
from myuw.dao.term import get_current_quarter


FDAO_SWS = 'restclients.dao_implementation.sws.File'


class TestCanvas(TestCase):
    def setUp(self):
        fake_request = RequestFactory()
        fake_request.session = {}
        UserServiceMiddleware().process_request(fake_request)

    def test_crosslinks(self):
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
