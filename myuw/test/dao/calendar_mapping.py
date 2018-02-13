from django.test import TestCase
from myuw.dao.calendar_mapping import \
    get_calendars_for_minors, get_calendars_for_majors, \
    get_calendars_for_gradmajors, _get_calendars,\
    _get_calendar_ids_from_text
from myuw.test import get_request_with_user, get_request_with_date


class TestCalendarMapping(TestCase):

    def test_get_by_major(self):
        req = get_request_with_user('jeos')
        enrollments = {'majors': ['NON MATRICULATED'],
                       'minors': []}
        cals = _get_calendars(req, enrollments)
        self.assertEqual(len(cals), 3)
        self.assertTrue('5_current' in cals)
        self.assertEqual(cals['5_current'],
                         'http://art.washington.edu/calendar/')

    def test_get_by_minor(self):
        req = get_request_with_user('javerage')
        enrollments = {'majors': [],
                       'minors': ['ASL']}
        cals = _get_calendars(req, enrollments)
        self.assertEqual(len(cals), 3)
        self.assertTrue('2_current' in cals)

        self.assertIsNone(cals['2_current'])

    def test_get_by_gradmajor(self):
        req = get_request_with_user('seagrad')
        enrollments = {'majors': ['ACMS (SOC & BEH SCI)'],
                       'minors': []}

        cals = _get_calendars(req, enrollments)
        self.assertEqual(len(cals), 3)
        self.assertIn('future_1', cals)
        self.assertIn('far_future', cals)
        self.assertIn('past', cals)

    def test_unknown_major(self):
        req = get_request_with_user('javerage')
        enrollments = {'majors': ['WTFBBQ'],
                       'minors': []}
        cals = _get_calendars(req, enrollments)
        self.assertEqual(len(cals), 0)

    def test_dupe_calendar(self):
        req = get_request_with_user('jeos')
        enrollments = {'majors': ['NON MATRICULATED'],
                       'minors': ['ASL']}
        cals = _get_calendars(req, enrollments)
        self.assertEqual(len(cals), 5)

    def test_ids_from_text(self):
        text = "sea_art sea_math sea_wtf"
        ids = _get_calendar_ids_from_text(text)
        self.assertEqual(len(ids), 3)
        self.assertEqual(ids[0], "sea_art")

        text = "sea_art"
        ids = _get_calendar_ids_from_text(text)
        self.assertEqual(len(ids), 1)
        self.assertEqual(ids[0], "sea_art")
