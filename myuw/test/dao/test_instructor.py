from django.test import TransactionTestCase
from myuw.dao.instructor import is_instructor, add_seen_instructor,\
    remove_seen_instructors_for_prior_terms, is_seen_instructor,\
    remove_seen_instructors_for_prior_years
from myuw.dao.term import get_specific_term
from myuw.test import get_request_with_user, get_request_with_date


class TestSeenInstructor(TransactionTestCase):
    def test_non_instructorness(self):
        self.assertEqual(is_seen_instructor('bill'), False)

    def test_is_seen_instructor(self):
        add_seen_instructor('bill', 2012, "autumn")
        self.assertEqual(is_seen_instructor('bill'), True)

    def test_remove_instructors_prior_terms(self):
        add_seen_instructor('bill', 2012, "summer")
        term = get_specific_term(2013, "autumn")
        remove_seen_instructors_for_prior_terms(term)
        req = get_request_with_user('bill',
                                    get_request_with_date("2013-04-10"))
        self.assertEqual(is_seen_instructor('bill'), False)

        add_seen_instructor('bill', 2013, "summer")
        term = get_specific_term(2013, "autumn")
        remove_seen_instructors_for_prior_terms(term)
        self.assertEqual(is_seen_instructor('bill'), True)
        self.assertTrue(is_instructor(req))

    def test_remove_instructors_prior_years(self):
        add_seen_instructor('bill', 2012, "autumn")
        req = get_request_with_user('bill',
                                    get_request_with_date("2013-04-10"))
        self.assertEqual(is_seen_instructor('bill'), True)

        remove_seen_instructors_for_prior_years(2013)
        self.assertEqual(is_seen_instructor('bill'), False)

    def test_is_instructor(self):
        request = get_request_with_user('bill',
                                        get_request_with_date("2013-04-10"))
        self.assertFalse(hasattr(request, "myuw_is_instructor"))
        self.assertTrue(is_instructor(request))
        self.assertTrue(hasattr(request, "myuw_is_instructor"))

        request = get_request_with_user('billsea',
                                        get_request_with_date("2013-04-10"))
        self.assertTrue(is_instructor(request))

        request = get_request_with_user('billseata',
                                        get_request_with_date("2013-04-10"))
        self.assertTrue(is_instructor(request))

        request = get_request_with_user('billpce',
                                        get_request_with_date("2013-04-10"))
        self.assertTrue(is_instructor(request))
