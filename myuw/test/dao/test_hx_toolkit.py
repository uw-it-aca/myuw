from datetime import datetime
from django.test import TestCase
from myuw.dao.affiliation import get_is_hxt_viewer
from myuw.dao.hx_toolkit_dao import (
    _get_week_between, _make_start_sunday, _get_phase_by_term,
    get_article_links, get_article_of_week_by_request, get_week_by_request)
from myuw.dao.term import get_current_quarter
from myuw.test import (get_request_with_date, get_request_with_user,
                       get_request, fdao_uwnetid_override)


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

    def test_is_hxt_viewer(self):
        request = get_request_with_user('javerage')
        self.assertTrue(get_is_hxt_viewer(request)[5])

        # not-sea
        request = get_request_with_user('tacgrad')
        self.assertFalse(get_is_hxt_viewer(request)[5])

        # not-ugrad
        request = get_request_with_user('botgrad')
        self.assertFalse(get_is_hxt_viewer(request)[5])

        # fyp
        request = get_request_with_user('jnew')
        self.assertFalse(get_is_hxt_viewer(request)[5])

        # au transfer in au MUWM-4798
        request = get_request_with_user('javg001',
                                        get_request_with_date("2017-09-18"))
        self.assertTrue(get_is_hxt_viewer(request)[5])

        # au transfter outside au
        request = get_request_with_user('javg001',
                                        get_request_with_date("2017-02-18"))
        self.assertTrue(get_is_hxt_viewer(request)[5])

        # wi transfer in wi MUWM-4798
        request = get_request_with_user('javg002',
                                        get_request_with_date("2017-02-18"))
        self.assertTrue(get_is_hxt_viewer(request)[5])

        # wi transfter outside wi
        request = get_request_with_user('javg002',
                                        get_request_with_date("2017-09-18"))
        self.assertTrue(get_is_hxt_viewer(request)[5])

    def test_get_article_links(self):
        links = get_article_links()
        self.assertEqual(len(links), 4)

    def test_get_article_of_week_by_request(self):
        request = get_request_with_user('javerage')
        self.assertEqual(get_week_by_request(request), 3)
        article = get_article_of_week_by_request(request)
        self.assertIsNotNone(article)
