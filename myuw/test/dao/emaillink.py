from django.test import TestCase
from myuw.dao.emaillink import get_service_url_for_address,\
    EmailServiceUrlException


class TestEmailServiceUrl(TestCase):

    def test_(self):
        addresses = [
            ("javerage@javerage.deskmail.washington.edu",
             ("https://alpine.washington.edu", "UW Deskmail", "fa-envelope")),
            ("javerage@gamail.uw.edu",
             ("https://mail.google.com", "UW Gmail", "fa-google")),
            ("javerage@exchange.washington.edu",
             ("https://outlook.office365.com", "UW Office 365", "fa-windows")),
            ("javerage@gmail.com",
             ("https://mail.google.com,GMail", "fa-google")),
            ("javerage@hotmail.com",
             ("https://mail.live.com/m", "Hotmail", "fa-windows")),
            ("javerage@yahoo.com",
             ("https://mail.yahoo.com", "Yahoo", "fa-yahoo")),
            ("javerage@comcast.net",
             ("https://login.comcast.net", "Comcast", "fa-envelope")),
            ("javerage@msn.com",
             ("https://www.msn.com", "MSN", "fa-windows")),
            ("javerage@aol.com",
             ("https://my.screenname.aol.com", "AOL", "fa-envelope")),
            ("javerage@live.com",
             ("https://mail.live.com/m", "MS Live", "fa-envelope")),
            ("javerage@163.com",
             ("https://mail.163.com/", "NetEase", "fa-envelope")),
            ("javerage@outlook.com",
             ("https://www.outlook.com", "Outlook", "fa-windows")),
            ("javerage@earthlink.net",
             ("https://webmail.earthlink.net", "EarthLink", "fa-envelope")),
            ("javerage@mac.com",
             ("https://www.icloud.com", "Mac Mail", "fa-apple")),
            ("javerage@me.com",
             ("https://www.icloud.com", "Mobile Me", "fa-apple")),
            ("javerage@126.com",
             ("https://mail.126.com", "NetEase", "fa-envelope")),
            ("javerage@qq.com",
             ("https://en.mail.qq.com/cgi-bin/loginpage", "QQMail",
              "fa-envelope")),
            ("javerage@icloud.com",
             ("https://www.icloud.com", "iCloud Mail", "fa-apple")),
        ]

        for address in addresses:
            url, title, icon = get_service_url_for_address(
                address[0])
        self.assertEquals(url, address[1][0])
        self.assertEquals(title, address[1][1])
        self.assertEquals(icon, address[1][2])

        with self.assertRaises(EmailServiceUrlException):
            get_service_url_for_address("user@unknowndomain.com")

        with self.assertRaises(EmailServiceUrlException):
            get_service_url_for_address("notanemailaddress")
