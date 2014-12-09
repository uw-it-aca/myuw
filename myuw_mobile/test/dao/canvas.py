from django.test import TestCase
from django.test.client import RequestFactory
from myuw_mobile.dao.canvas import get_indexed_data_for_regid
from myuw_mobile.dao.canvas import get_indexed_by_decrosslisted
from myuw_mobile.dao.schedule import _get_schedule
from myuw_mobile.dao.term import get_current_quarter

class TestCanvas(TestCase):
    def test_crosslinks(self):
        with self.settings(
            RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):

            data = get_indexed_data_for_regid("12345678901234567890123456789012")
            physics = data['2013,spring,PHYS,121/A']
            self.assertEquals(physics.course_url, 'https://canvas.uw.edu/courses/149650')

            train = data['2013,spring,TRAIN,100/B']
            self.assertEquals(train.course_url, 'https://canvas.uw.edu/courses/249650')


    def test_crosslinks_lookup(self):
        with self.settings(
            RESTCLIENTS_SWS_DAO_CLASS='restclients.dao_implementation.sws.File'):

            data = get_indexed_data_for_regid("12345678901234567890123456789012")

            now_request = RequestFactory().get("/")
            now_request.session = {}
            term = get_current_quarter(now_request)
            schedule = _get_schedule("12345678901234567890123456789012", term)
            canvas_data_by_course_id = get_indexed_by_decrosslisted(data, schedule.sections)

            physics = data['2013,spring,PHYS,121/A']
            self.assertEquals(physics.course_url, 'https://canvas.uw.edu/courses/149650')

            train = data['2013,spring,TRAIN,100/A']
            self.assertEquals(train.course_url, 'https://canvas.uw.edu/courses/249650')
