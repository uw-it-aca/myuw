from django.test import TestCase
from myuw.dao.exceptions import EmailServiceUrlException
from myuw.dao.emaillink import get_service_url_for_address
from restclients.uwnetid.subscription import get_email_forwarding


class TestEnrollment(TestCase):

    def test_get_enrollment_quarter(self):
        pass

    def test_get_all_enrollment(self):
        pass
