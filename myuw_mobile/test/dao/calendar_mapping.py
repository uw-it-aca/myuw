from django.test import TestCase
from django.test.client import RequestFactory
from myuw_mobile.dao.calendar_mapping import \
    get_calendars_for_minors, get_calendars_for_majors, \
    get_calendars_for_gradmajors, _get_enrollments

class TestCalendarMapping(TestCase):
    def test_get_by_major(self):
        cals = get_calendars_for_majors(['TRAIN'])
        self.assertEqual(len(cals), 1)
        self.assertEqual(cals[0].calendar_id, 'sea_art')
        self.assertEqual(cals[0].base_url, 'http://art.washington.edu/calendar/')

    def test_get_by_minor(self):
        cals = get_calendars_for_minors(['TRAIN'])
        self.assertEqual(len(cals), 1)
        self.assertEqual(cals[0].calendar_id, 'organic')
        self.assertIsNone(cals[0].base_url)

    def test_get_by_gradmajor(self):
        cals = get_calendars_for_gradmajors(['TRAIN'])
        self.assertEqual(len(cals), 2)
        cal_ids = [cal.calendar_id for cal in cals]
        self.assertIn('organic', cal_ids)
        self.assertIn('sea_art', cal_ids)
        for cal in cals:
            self.assertIsNone(cal.base_url)

    def test_no_calendar(self):
        cals = get_calendars_for_gradmajors(['TRAINS'])
        self.assertEqual(len(cals), 0)

    def test_unknown_major(self):
        cals = get_calendars_for_gradmajors(['WTFBBQ'])
        self.assertEqual(len(cals), 0)

    def test_dupe_calendar(self):
        cals = get_calendars_for_gradmajors(['TRAINR', 'TRAIN'])
        self.assertEqual(len(cals), 2)
