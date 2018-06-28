from django.test import TransactionTestCase
from myuw.models import Instructor
from myuw.dao.instructor import is_instructor
from myuw.dao.user import get_user_model
from myuw.test import get_request_with_user, get_request_with_date,\
    fdao_pws_override, fdao_sws_override


@fdao_pws_override
@fdao_sws_override
class TestInstructor(TransactionTestCase):
    def test_non_instructorness(self):
        req = get_request_with_user('bill')
        user = get_user_model(req)
        self.assertFalse(Instructor.is_seen_instructor(user))

    def test_is_seen_instructor(self):
        req = get_request_with_user('bill')
        user = get_user_model(req)
        Instructor.add_seen_instructor(user, 2012, "autumn")
        self.assertTrue(Instructor.is_seen_instructor(user))

    def test_remove_seen_instructors_yrs_before(self):
        req = get_request_with_user('bill')
        user = get_user_model(req)
        Instructor.add_seen_instructor(user, 2012, "autumn")
        self.assertTrue(Instructor.is_seen_instructor(user))
        Instructor.remove_seen_instructors_yrs_before(2013)
        self.assertFalse(Instructor.is_seen_instructor(user))

        Instructor.add_seen_instructor(user, 2013, "winter")
        Instructor.remove_seen_instructors_yrs_before(2013)
        self.assertTrue(Instructor.is_seen_instructor(user))

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
