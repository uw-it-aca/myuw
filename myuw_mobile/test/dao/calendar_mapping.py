from django.test import TestCase
from django.test.client import RequestFactory
from myuw_mobile.dao.calendar_mapping import \
    get_calendars_for_minors, get_calendars_for_majors, \
    get_calendars_for_gradmajors, _get_enrollments, \
    _get_calendars


class TestCalendarMapping(TestCase):
    def test_get_by_major(self):
        enrollments = {'majors': ['TRAIN'],
                       'minors': [],
                       'is_grad': False}

        cals = _get_calendars(enrollments)
        self.assertEqual(len(cals), 3)
        self.assertTrue('5_current' in cals)
        self.assertEqual(cals['5_current'],
                         'http://art.washington.edu/calendar/')

    def test_get_by_minor(self):
        enrollments = {'majors': [],
                       'minors': ['TRAINR'],
                       'is_grad': False}

        cals = _get_calendars(enrollments)
        self.assertEqual(len(cals), 3)
        self.assertTrue('2_current' in cals)

        self.assertIsNone(cals['2_current'])

    def test_get_by_gradmajor(self):
        enrollments = {'majors': ['UPCOM'],
                       'minors': [],
                       'is_grad': True}

        cals = _get_calendars(enrollments)
        self.assertEqual(len(cals), 3)
        self.assertIn('future_1', cals)
        self.assertIn('far_future', cals)
        self.assertIn('past', cals)


    def test_unknown_major(self):
        enrollments = {'majors': ['WTFBBQ'],
                       'minors': [],
                       'is_grad': False}
        cals = _get_calendars(enrollments)
        self.assertEqual(len(cals), 0)

    def test_dupe_calendar(self):
        enrollments = {'majors': ['TRAIN'],
                       'minors': ['TRAINR'],
                       'is_grad': False}
        cals = _get_calendars(enrollments)
        self.assertEqual(len(cals), 5)
