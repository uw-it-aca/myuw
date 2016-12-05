from django.test import TestCase
from myuw.dao.canvas import get_indexed_data_for_regid
from myuw.dao.canvas import get_indexed_by_decrosslisted
from myuw.dao.schedule import _get_schedule
from myuw.dao.term import get_current_quarter
from myuw.test import fdao_sws_override, get_request_with_user, get_request


@fdao_sws_override
class TestCanvas(TestCase):
    def setUp(self):
        get_request()

    def test_crosslinks(self):
        data = get_indexed_data_for_regid(
            "12345678901234567890123456789012")
        physics = data['2013,spring,PHYS,121/A'].course
        self.assertEquals(physics.course_url,
                          'https://canvas.uw.edu/courses/249652')
        self.assertFalse(physics.is_unpublished())

        has_section_b = '2013,spring,TRAIN,100/B' in data
        self.assertTrue(has_section_b)

        has_section_a = '2013,spring,TRAIN,100/A' in data
        self.assertTrue(has_section_a)

        train = data['2013,spring,TRAIN,100/A'].course
        self.assertEquals(train.course_url,
                          'https://canvas.uw.edu/courses/249650')
        self.assertFalse(physics.is_unpublished())

    def test_crosslinks_lookup(self):
        data = get_indexed_data_for_regid(
            "12345678901234567890123456789012")

        now_request = get_request_with_user('javerage')
        term = get_current_quarter(now_request)
        schedule = _get_schedule("12345678901234567890123456789012", term)
        canvas_data_by_course_id = get_indexed_by_decrosslisted(
            data, schedule.sections)

        physics = data['2013,spring,PHYS,121/A'].course
        self.assertEquals(physics.course_url,
                          'https://canvas.uw.edu/courses/249652')
        self.assertFalse(physics.is_unpublished())

        has_section_a = '2013,spring,TRAIN,100/A' in data
        self.assertTrue(has_section_a)

        train = data['2013,spring,TRAIN,100/A'].course
        self.assertEquals(train.course_url,
                          'https://canvas.uw.edu/courses/249650')
        self.assertTrue(train.is_unpublished())
