from django.test import TestCase
from myuw.dao.exceptions import EmailServiceUrlException
from myuw.dao.emaillink import get_service_url_for_address
from restclients.uwnetid.subscription import get_email_forwarding


class TestEmailServiceUrl(TestCase):

    def test_(self):
        netids = [('javerage', "http://gmail.uw.edu"),
                  ('javg001', "http://alpine.washington.edu"),
                  ('javg002', "https://outlook.office365.com"),
                  ('javg003', "https://mail.google.com"),
                  ('javg004', "https://mail.live.com"),
                  ('javg005', "https://mail.yahoo.com"),
                  ('javg006', "https://login.comcast.net"),
                  ('javg007', "https://mail.live.com"),
                  ('javg008', "https://my.screenname.aol.com"),
                  ('javg009', "https://mail.live.com"),
                  ('javg010', "https://mail.163.com"),
                  ('javg011', "https://www.outlook.com"),
                  ('javg012', "https://webmail.earthlink.net"),
                  ('javg013', "https://www.icloud.com"),
                  ('javg014', "https://www.icloud.com"),
                  ('javg015', "https://mail.126.com"),
                  ('javg016', "https://en.mail.qq.com"),
                  ('javg017', "https://www.icloud.com")]

        for netid in netids:
            fwd = get_email_forwarding(netid[0])
            url, title, icon = get_service_url_for_address(fwd.fwd)
            self.assertEquals(url, netid[1])
            self.assertGreater(len(title), 0)
            self.assertGreater(len(icon), 0)

        with self.assertRaises(EmailServiceUrlException):
            get_service_url_for_address("user@unknowndomain.com")

        with self.assertRaises(EmailServiceUrlException):
            get_service_url_for_address("notanemailaddress")

        with self.assertRaises(EmailServiceUrlException):
            get_service_url_for_address({})
