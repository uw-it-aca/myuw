from django.test import TestCase
from django.conf import settings
from restclients_core.exceptions import DataFailureException
from uw_sws.models import Section, Person
from myuw.dao.term import get_current_quarter, get_next_quarter
from myuw.dao.enrollment import find_enrolled_independent_start_section
from myuw.test import fdao_sws_override, fdao_pws_override,\
    get_request_with_date, get_request, get_request_with_user


@fdao_pws_override
@fdao_sws_override
class TestEnrollment(TestCase):
    def setUp(self):
        get_request()

    def test_find_enrolled_independent_start_section(self):
        req = get_request_with_user('jpce',
                                    get_request_with_date("2013-01-10"))
        isection, ended = find_enrolled_independent_start_section(
            req, '2013,winter,COM,201/A')
        self.assertEqual(str(isection.end_date), '2013-04-29 00:00:00')
        self.assertFalse(ended)

        isection, ended = find_enrolled_independent_start_section(
            req, '2013,winter,PSYCH,203/A')
        self.assertEqual(str(isection.end_date), '2013-06-22 00:00:00')
        self.assertFalse(ended)
