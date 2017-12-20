from datetime import datetime
from django.test import TestCase
from myuw.test import (get_request_with_date, get_request_with_user,
                       get_request, fdao_uwnetid_override)
from myuw.dao.term import get_current_quarter
from myuw.dao.hx_toolkit_dao import _get_week_between, _make_start_sunday, \
    _get_phase_by_term


@fdao_uwnetid_override
class TestHXTDao(TestCase):
    def setUp(self):
        get_request()

    def test_get_weeks(self):
        now_request = get_request_with_date('2013-01-20')
        request = get_request_with_user('javerage', now_request)
        term = get_current_quarter(request)
        # term first day: 2013-01-07
        before = datetime(2013, 1, 1).date()
        week = _get_week_between(term, before)
        self.assertEqual(week, -1)

        before_same_wk = datetime(2013, 1, 6).date()
        week = _get_week_between(term, before_same_wk)
        self.assertEqual(week, 1)

        start = datetime(2013, 1, 7).date()
        week = _get_week_between(term, start)
        self.assertEqual(week, 1)

        after_same_wk = datetime(2013, 1, 8).date()
        week = _get_week_between(term, after_same_wk)
        self.assertEqual(week, 1)

        after = datetime(2013, 2, 1).date()
        week = _get_week_between(term, after)
        self.assertEqual(week, 4)

    def test_make_start_sunday(self):
        sunday = _make_start_sunday(datetime(2013, 1, 5).date())
        self.assertEqual(sunday.weekday(), 6)

        sunday = _make_start_sunday(datetime(2013, 1, 6).date())
        self.assertEqual(sunday.weekday(), 6)

        sunday = _make_start_sunday(datetime(2013, 1, 7).date())
        self.assertEqual(sunday.weekday(), 6)

    def test_get_phase(self):
        now_request = get_request_with_date('2013-01-20')
        request = get_request_with_user('javerage', now_request)
        term = get_current_quarter(request)
        self.assertEqual(_get_phase_by_term(term), 'B')

        now_request = get_request_with_date('2012-10-28')
        request = get_request_with_user('javerage', now_request)
        term = get_current_quarter(request)
        self.assertEqual(_get_phase_by_term(term), 'B')

