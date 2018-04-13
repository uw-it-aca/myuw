from django.test import TestCase
from django.conf import settings
from uw_sws.models import ClassSchedule, Term, Section, Person
from myuw.dao.term import get_specific_term, get_next_non_summer_quarter,\
    is_a_term, is_b_term, is_full_summer_term
from myuw.dao.registration import get_schedule_by_term
from myuw.dao.registered_term import _get_registered_summer_terms,\
    _must_displayed_separately, _get_registered_future_quarters,\
    save_seen_registration_obj
from myuw.dao.user import get_user_model
from myuw.models import SeenRegistration
from myuw.test import get_request_with_date, get_request_with_user,\
    fdao_sws_override, fdao_pws_override


@fdao_pws_override
@fdao_sws_override
class TestRegisteredTerm(TestCase):

    def test_get_registered_summer_terms(self):
        req = get_request_with_user('javerage')
        term = get_specific_term(2013, "summer")
        schedule = get_schedule_by_term(req, term)
        data = _get_registered_summer_terms(schedule.sections)
        self.assertTrue(data["B"])
        self.assertTrue(data["A"])

    def test_must_displayed_separately(self):
        req = get_request_with_user('javerage')
        term = get_specific_term(2013, "summer")
        schedule = get_schedule_by_term(req, term)
        self.assertTrue(_must_displayed_separately(schedule))

    def test_get_registered_future_quarters(self):
        req = get_request_with_user('javerage')
        term1 = get_specific_term(2013, "summer")
        schedule1 = get_schedule_by_term(req, term1)
        self.assertEqual(len(schedule1.sections), 3)

        term2 = get_specific_term(2013, "autumn")
        schedule2 = get_schedule_by_term(req, term2)
        self.assertEqual(len(schedule2.sections), 2)

        terms = _get_registered_future_quarters(req, schedule1, schedule2)
        self.assertTrue(len(terms) == 3)
        self.assertTrue(terms[0]['year'] == 2013)
        self.assertEqual(terms[0]['quarter'], "Summer")
        self.assertEqual(terms[0]['summer_term'], "a-term")

        self.assertTrue(terms[1]['year'] == 2013)
        self.assertEqual(terms[1]['quarter'], "Summer")
        self.assertEqual(terms[1]['summer_term'], "b-term")

        self.assertTrue(terms[2]['year'] == 2013)
        self.assertEqual(terms[2]['quarter'], "Autumn")
        self.assertEqual(terms[2]['summer_term'], "")

        terms = _get_registered_future_quarters(req, None, None)
        self.assertEqual(len(terms), 0)

        # MUWM-3010
        # Baseline pre-summer
        now_request = get_request_with_user(
            'javerage', get_request_with_date("2013-04-01"))
        terms = _get_registered_future_quarters(now_request,
                                                schedule1,
                                                schedule2)
        self.assertTrue(len(terms) == 3)
        self.assertTrue(terms[0]['year'] == 2013)
        self.assertEqual(terms[0]['quarter'], "Summer")
        self.assertEqual(terms[0]['summer_term'], "a-term")

        self.assertTrue(terms[1]['year'] == 2013)
        self.assertEqual(terms[1]['quarter'], "Summer")
        self.assertEqual(terms[1]['summer_term'], "b-term")

        self.assertTrue(terms[2]['year'] == 2013)
        self.assertEqual(terms[2]['quarter'], "Autumn")
        self.assertEqual(terms[2]['summer_term'], "")

        # Summer has started - so no a-term
        now_request = get_request_with_user(
            'javerage', get_request_with_date("2013-06-30"))
        terms = _get_registered_future_quarters(now_request, schedule1,
                                                schedule2)
        self.assertTrue(len(terms) == 2)

        self.assertTrue(terms[0]['year'] == 2013)
        self.assertEqual(terms[0]['quarter'], "Summer")
        self.assertEqual(terms[0]['summer_term'], "b-term")

        self.assertTrue(terms[1]['year'] == 2013)
        self.assertEqual(terms[1]['quarter'], "Autumn")
        self.assertEqual(terms[1]['summer_term'], "")

        # Summer b-term has started - so no a-term or b-term
        now_request = get_request_with_user(
            'javerage', get_request_with_date("2013-07-30"))
        terms = _get_registered_future_quarters(now_request, schedule1,
                                                schedule2)
        self.assertTrue(len(terms) == 1)

        self.assertTrue(terms[0]['year'] == 2013)
        self.assertEqual(terms[0]['quarter'], "Autumn")
        self.assertEqual(terms[0]['summer_term'], "")

        now_request = get_request_with_user(
            'javerage', get_request_with_date("2013-12-10"))
        term = get_specific_term(2014, "winter")
        winter2014_sche = get_schedule_by_term(now_request, term)
        self.assertIsNotNone(winter2014_sche)
        self.assertEqual(len(winter2014_sche.sections), 5)
        registered_future_quarters =\
            _get_registered_future_quarters(now_request,
                                            winter2014_sche,
                                            None)

        self.assertEqual(len(registered_future_quarters), 1)
        term1 = registered_future_quarters[0]
        self.assertEqual(term1["quarter"], "Winter")
        self.assertEqual(term1["year"], 2014)
        self.assertEqual(term1["section_count"], 5)

    def test_save_seen_registration_obj(self):
        now_request = get_request_with_user(
            'javerage', get_request_with_date("2013-12-10"))
        term = get_specific_term(2014, "winter")
        winter2014_sche = get_schedule_by_term(now_request, term)
        self.assertIsNotNone(winter2014_sche)
        self.assertEqual(len(winter2014_sche.sections), 5)
        registered_future_quarters = _get_registered_future_quarters(
            now_request,  winter2014_sche, None)

        user = get_user_model(now_request)
        model, created, now_datetime, summer_term =\
            save_seen_registration_obj(user, now_request,
                                       registered_future_quarters[0])
        self.assertTrue(created)
        self.assertEqual(model.user.uwnetid, "javerage")
        self.assertEqual(model.year, 2014)
        self.assertEqual(model.quarter, "Winter")
        self.assertEqual(model.summer_term, "F")
        qset = SeenRegistration.objects.filter(user=user,
                                               year=2014,
                                               quarter="Winter",
                                               summer_term="F",
                                               )
        self.assertEqual(len(qset), 1)

        model1, created1, now_datetime1, summer_term1 =\
            save_seen_registration_obj(user, now_request,
                                       registered_future_quarters[0])
        self.assertFalse(created1)
        qset1 = SeenRegistration.objects.filter(user=user,
                                                year=2014,
                                                quarter="Winter",
                                                summer_term="F",
                                                )
        self.assertEqual(len(qset1), 1)

        now_request = get_request_with_user(
            'javerage', get_request_with_date("2013-5-10"))
        term = get_specific_term(2013, "summer")
        summer2013_sche = get_schedule_by_term(now_request, term)
        self.assertIsNotNone(summer2013_sche)
        self.assertEqual(len(summer2013_sche.sections), 3)
        registered_future_quarters = _get_registered_future_quarters(
            now_request,  summer2013_sche, None)
        self.assertEqual(len(registered_future_quarters), 2)

        quarter = registered_future_quarters[0]
        model, created, now_datetime, summer_term =\
            save_seen_registration_obj(user, now_request,
                                       quarter)
        self.assertTrue(created)
        self.assertEqual(model.user.uwnetid, "javerage")
        self.assertEqual(model.year, 2013)
        self.assertEqual(model.quarter, "Summer")
        self.assertEqual(model.summer_term, "A")
        qset = SeenRegistration.objects.filter(user=user,
                                               year=2013,
                                               quarter="Summer",
                                               summer_term="A",
                                               )
        self.assertEqual(len(qset), 1)

        model1, created1, now_datetime1, summer_term1 =\
            save_seen_registration_obj(user, now_request,
                                       quarter)
        self.assertFalse(created1)
        qset1 = SeenRegistration.objects.filter(user=user,
                                                year=2013,
                                                quarter="Summer",
                                                summer_term="A",
                                                )
        self.assertEqual(len(qset1), 1)

        quarter = registered_future_quarters[1]
        model, created, now_datetime, summer_term =\
            save_seen_registration_obj(user, now_request,
                                       quarter)
        self.assertTrue(created)
        self.assertEqual(model.user.uwnetid, "javerage")
        self.assertEqual(model.year, 2013)
        self.assertEqual(model.quarter, "Summer")
        self.assertEqual(model.summer_term, "B")
        qset = SeenRegistration.objects.filter(user=user,
                                               year=2013,
                                               quarter="Summer",
                                               summer_term="B",
                                               )
        self.assertEqual(len(qset), 1)

        model1, created1, now_datetime1, summer_term1 =\
            save_seen_registration_obj(user, now_request,
                                       quarter)
        self.assertFalse(created1)
        qset1 = SeenRegistration.objects.filter(user=user,
                                                year=2013,
                                                quarter="Summer",
                                                summer_term="B",
                                                )
        self.assertEqual(len(qset1), 1)
