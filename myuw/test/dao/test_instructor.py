from django.test import TransactionTestCase
from myuw.dao.instructor import is_instructor, add_seen_instructor,\
    is_seen_instructor, remove_seen_instructors_yrs_before
from myuw.dao.term import get_specific_term
from myuw.test import get_request_with_user, get_request_with_date


class TestSeenInstructor(TransactionTestCase):
    def test_non_instructorness(self):
        self.assertFalse(is_seen_instructor('bill'))

    def test_is_seen_instructor(self):
        add_seen_instructor('bill', 2012, "autumn")
        self.assertTrue(is_seen_instructor('bill'))

    def test_remove_seen_instructors_yrs_before(self):
        add_seen_instructor('bill', 2012, "autumn")
        self.assertTrue(is_seen_instructor('bill'))
        remove_seen_instructors_yrs_before(2013)
        self.assertFalse(is_seen_instructor('bill'))

        add_seen_instructor('bill', 2013, "winter")
        remove_seen_instructors_yrs_before(2013)
        self.assertTrue(is_seen_instructor('bill'))

    def test_instructor_3_term_before(self):
        req = get_request_with_user('bill',
                                    get_request_with_date("2014-04-10"))
        self.assertFalse(hasattr(req, "myuw_is_instructor"))
        self.assertFalse(is_instructor(req))
        self.assertFalse(req.myuw_is_instructor)

    def test_is_instructor(self):
        req = get_request_with_user('bill',
                                    get_request_with_date("2013-04-10"))
        self.assertTrue(is_instructor(req))
        # get the one cached in the req
        self.assertTrue(is_instructor(req))

        # taught in last term
        req = get_request_with_user('billsea',
                                    get_request_with_date("2014-01-10"))
        self.assertTrue(is_instructor(req))

        req = get_request_with_user('billseata',
                                    get_request_with_date("2013-04-10"))
        self.assertTrue(is_instructor(req))

        req = get_request_with_user('billpce',
                                    get_request_with_date("2013-04-10"))
        self.assertTrue(is_instructor(req))
