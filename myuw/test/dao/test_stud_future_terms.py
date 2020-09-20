from django.test import TransactionTestCase
from django.conf import settings
from restclients_core.exceptions import DataFailureException
from myuw.dao.stud_future_terms import get_registered_future_quarters
from myuw.dao.user import get_user_model
from myuw.models import SeenRegistration
from myuw.test import get_request_with_date, get_request_with_user,\
    fdao_sws_override, fdao_pws_override


@fdao_pws_override
@fdao_sws_override
class TestRegisteredTerm(TransactionTestCase):

    def test_no_future_quarter_regs(self):
        req = get_request_with_user('none')
        self.assertRaises(DataFailureException,
                          get_registered_future_quarters, req)

        req = get_request_with_user('staff')
        self.assertRaises(DataFailureException,
                          get_registered_future_quarters, req)

    def test_get_registered_future_quarters(self):
        req = get_request_with_user('javerage')
        data = get_registered_future_quarters(req)
        terms = data.get("terms")
        self.assertEqual(len(terms), 3)
        self.assertEqual(terms[0]['year'], 2013)
        self.assertEqual(terms[0]['quarter'], "Summer")
        self.assertEqual(terms[0]['summer_term'], "a-term")
        self.assertEqual(terms[0]['url'], '/2013,summer,a-term')
        self.assertEqual(terms[0]['credits'], '2.0')
        self.assertEqual(terms[0]['section_count'], 2)
        self.assertTrue(terms[0]['has_registration'])

        self.assertEqual(terms[1]['year'], 2013)
        self.assertEqual(terms[1]['quarter'], "Summer")
        self.assertEqual(terms[1]['summer_term'], "b-term")
        self.assertEqual(terms[1]['url'], '/2013,summer,b-term')
        self.assertEqual(terms[1]['credits'], '3.0')
        self.assertEqual(terms[1]['section_count'], 2)

        self.assertEqual(terms[2]['year'], 2013)
        self.assertEqual(terms[2]['quarter'], "Autumn")
        self.assertIsNone(terms[2]['summer_term'])
        self.assertEquals(data['next_term_data']['label'], '2013,autumn')

        # Summer has started - exclude a-term
        req = get_request_with_user(
            'javerage', get_request_with_date("2013-06-24"))
        data = get_registered_future_quarters(req)
        terms = data["terms"]
        self.assertEqual(len(terms), 2)
        self.assertTrue(terms[0]['year'] == 2013)
        self.assertEqual(terms[0]['quarter'], "Summer")
        self.assertEqual(terms[0]['summer_term'], "b-term")

        self.assertTrue(terms[1]['year'] == 2013)
        self.assertEqual(terms[1]['quarter'], "Autumn")
        self.assertEqual(data["next_term_data"]['year'], 2013)
        self.assertEqual(data["next_term_data"]['quarter'], "Autumn")

        # Summer b-term has started
        req = get_request_with_user(
            'javerage', get_request_with_date("2013-07-25"))
        data = get_registered_future_quarters(req)
        terms = data["terms"]
        self.assertTrue(len(terms) == 1)
        self.assertTrue(terms[0]['year'] == 2013)
        self.assertEqual(terms[0]['quarter'], "Autumn")

        # Winter quarter enrollment
        req = get_request_with_user(
            'javerage', get_request_with_date("2013-11-10"))
        data = get_registered_future_quarters(req)
        terms = data["terms"]
        self.assertTrue(len(terms) == 1)
        self.assertEqual(terms[0]["quarter"], "Winter")
        self.assertEqual(terms[0]["year"], 2014)
        self.assertEqual(terms[0]['credits'], '15.0')
        self.assertEqual(terms[0]["section_count"], 5)
        self.assertTrue(terms[0]['has_registration'])

        req = get_request_with_user('eight')
        data = get_registered_future_quarters(req)
        terms = data.get("terms")
        self.assertEqual(len(terms), 3)
        self.assertEqual(terms[0]['year'], 2013)
        self.assertEqual(terms[0]['quarter'], "Summer")
        self.assertEqual(terms[0]['summer_term'], "a-term")
        self.assertEqual(terms[0]['url'], '/2013,summer,a-term')
        self.assertEqual(terms[0]['credits'], '6.0')
        self.assertEqual(terms[0]['section_count'], 2)
        self.assertTrue(terms[0]['has_registration'])

        self.assertEqual(terms[1]['year'], 2013)
        self.assertEqual(terms[1]['quarter'], "Summer")
        self.assertEqual(terms[1]['summer_term'], "b-term")
        self.assertEqual(terms[1]['url'], '/2013,summer,b-term')
        self.assertEqual(terms[1]['credits'], '6.0')
        self.assertEqual(terms[1]['section_count'], 2)

        self.assertEqual(terms[2]['year'], 2013)
        self.assertEqual(terms[2]['quarter'], "Autumn")
        self.assertEqual(terms[2]['section_count'], 1)
        self.assertEqual(terms[2]['credits'], '5.0')
        self.assertEquals(data['next_term_data']['label'], '2013,autumn')

        req = get_request_with_user(
            'jbothell', get_request_with_date("2013-01-05"))
        data = get_registered_future_quarters(req)
        terms = data.get("terms")
        self.assertEqual(len(terms), 1)
        self.assertEquals(data['next_term_data']['label'], '2013,spring')
        self.assertEqual(data['next_term_data']['section_count'], 4)

        req = get_request_with_user('jbothell')
        data = get_registered_future_quarters(req)
        terms = data.get("terms")
        self.assertEqual(len(terms), 1)
        self.assertEqual(data['next_term_data']['label'], '2013,autumn')
        self.assertEqual(data['next_term_data']['section_count'], 0)

        req = get_request_with_user(
            'jpce', get_request_with_date("2013-01-05"))
        data = get_registered_future_quarters(req)
        terms = data.get("terms")
        self.assertEqual(len(terms), 1)
        self.assertEqual(terms[0]['section_count'], 5)

        req = get_request_with_user('jpce')
        data = get_registered_future_quarters(req)
        terms = data.get("terms")
        self.assertEqual(len(terms), 3)
        self.assertEqual(terms[0]['url'], '/2013,summer,a-term')
        self.assertEqual(terms[0]['section_count'], 1)
        self.assertEqual(terms[1]['url'], '/2013,summer,b-term')
        self.assertEqual(terms[1]['section_count'], 2)
        self.assertEqual(terms[2]['url'], '/2013,autumn')
        self.assertEqual(terms[2]['section_count'], 0)

        req = get_request_with_user('jeos')
        data = get_registered_future_quarters(req)
        terms = data.get("terms")
        self.assertEqual(len(terms), 2)
        self.assertEqual(terms[0]['label'], '2013,summer')
        self.assertEqual(terms[0]['section_count'], 1)
        self.assertEqual(data['next_term_data']['label'], '2013,autumn')
        self.assertEqual(data['next_term_data']['section_count'], 1)

    def test_highlight(self):
        req = get_request_with_user(
            'javerage', get_request_with_date("2013-12-10"))
        data = get_registered_future_quarters(req)
        self.assertTrue(data["highlight_future_quarters"])
        self.assertTrue(data["terms"][0]["highlight"])
        user = get_user_model(req)
        qset = SeenRegistration.objects.filter(user=user,
                                               year=2014,
                                               quarter="Winter")
        self.assertEqual(len(qset), 1)
        model = qset[0]
        self.assertEqual(model.user.uwnetid, "javerage")
        self.assertEqual(model.year, 2014)
        self.assertEqual(model.quarter, "Winter")

        req = get_request_with_user(
            'javerage', get_request_with_date("2013-05-20"))
        data = get_registered_future_quarters(req)
        terms = data["terms"]
        self.assertEqual(len(terms), 3)
        self.assertTrue(data["terms"][0]["highlight"])
        self.assertTrue(data["terms"][1]["highlight"])
        self.assertTrue(data["terms"][2]["highlight"])
        self.assertTrue(data["highlight_future_quarters"])
        qset = SeenRegistration.objects.filter(user=user, year=2013,
                                               quarter="Summer")
        self.assertEqual(len(qset), 2)
        self.assertEqual(qset[0].summer_term, "a")
        self.assertEqual(qset[1].summer_term, "b")

        req = get_request_with_user(
            'javerage', get_request_with_date("2013-05-22"))
        data = get_registered_future_quarters(req)
        self.assertFalse(data["highlight_future_quarters"])

        req = get_request_with_user(
            'javerage', get_request_with_date("2013-07-10"))
        data = get_registered_future_quarters(req)
        self.assertEqual(len(data["terms"]), 2)
        self.assertFalse(data["terms"][0]["highlight"])
        self.assertFalse(data["terms"][1]["highlight"])
        self.assertFalse(data["highlight_future_quarters"])
        qset = SeenRegistration.objects.filter(user=user,
                                               year=2013,
                                               quarter="Summer")
        self.assertEqual(len(qset), 2)

        # MUWM-3009
        req = get_request_with_user(
            'javerage', get_request_with_date("2013-07-17"))
        data = get_registered_future_quarters(req)
        self.assertEqual(len(data["terms"]), 2)
        self.assertTrue(data["terms"][0]["highlight"])
        self.assertFalse(data["terms"][1]["highlight"])
        self.assertTrue(data["highlight_future_quarters"])
