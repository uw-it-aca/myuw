from django.test import TestCase
from django.conf import settings

from myuw_mobile.dao.links import Link as LinkDAO
from myuw_mobile.models import Link

class TestLinks(TestCase):
    def test_get_link_by_ID(self):
        ids = [10, 40, 60, 103, 104, 110]
        titles = ["Campus Maps", "Email - UW Gmail", "Grade Report", "Time Schedule - Tacoma", "Time Schedule - UW Professional & Continuing Education", "Tuition Charge Statement"]
        for i in range (len(ids)):
            link = LinkDAO.get_link_by_id(ids[i])
            link_name = link.title
            self.assertEquals(link_name, titles[i])