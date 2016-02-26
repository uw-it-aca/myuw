from django.test import TestCase
from restclients.exceptions import DataFailureException
from myuw.dao.uwemail import _get_email_forwarding_by_uwnetid


class TestUwEmail(TestCase):

    def test_get_by_netid(self):
        forward = _get_email_forwarding_by_uwnetid('javerage')
        self.assertEquals(forward.fwd, "javerage@gamail.uw.edu")
        forward = _get_email_forwarding_by_uwnetid(None)
        self.assertIsNone(forward)
        self.assertRaises(DataFailureException,
                          _get_email_forwarding_by_uwnetid,
                          "notarealnetid")
