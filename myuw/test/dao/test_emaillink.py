# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from myuw.dao.exceptions import EmailServiceUrlException
from myuw.dao.emaillink import get_service_url_for_address
from myuw.dao.uwnetid import get_email_forwarding_for_current_user
from myuw.test import get_request_with_user


class TestEmailServiceUrl(TestCase):

    def test_(self):
        netids = [('javerage', "http://gmail.uw.edu"),
                  ('retirestaff', "http://outlook.com/myuw.net"),
                  ('jeos', "https://exchange.uwmedicine.org"),
                  ('jpce', "https://mail.uwmed.org"),
                  ('seagrad', "https://mail.uwmed.org"),
                  ('javg001', "http://alpine.washington.edu"),
                  ('javg002', "https://outlook.office365.com/uw.edu"),
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
            req = get_request_with_user(netid[0])
            fwd = get_email_forwarding_for_current_user(req)
            url = get_service_url_for_address(fwd.fwd)
            self.assertEquals(url, netid[1])

        with self.assertRaises(EmailServiceUrlException):
            get_service_url_for_address("user@unknowndomain.com")

        with self.assertRaises(EmailServiceUrlException):
            get_service_url_for_address("notanemailaddress")

        with self.assertRaises(EmailServiceUrlException):
            get_service_url_for_address({})
