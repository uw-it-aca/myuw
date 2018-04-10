from django.test import TestCase
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from myuw.dao.category_links import _get_links_by_category_and_campus, \
    Res_Links, Resource_Links
from myuw.models.res_category_link import ResCategoryLink
from myuw.test import get_request_with_user
import re


class TestCategoryLinks(TestCase):

    def _test_ascii(self, s):
        try:
            s.decode('ascii')  # python 2
        except AttributeError:
            s.encode('ascii')  # python 3

    def test_get_all_links(self):
        all_links = Res_Links.get_all_links()
        self.assertEquals(len(all_links), 212)
        val = URLValidator()
        for link in all_links:
            try:
                self._test_ascii(link.url)
            except (UnicodeDecodeError, UnicodeEncodeError):
                self.fail("%s url has non-ASCII text: %s" %
                          (link.title, link.url))

            try:
                val(link.url)
            except ValidationError:
                # allow relative references
                if not re.match(r'^/[\w/]+$', link.url):
                    self.fail("Invalid url:" + link.url)

            try:
                self._test_ascii(link.title)
            except (UnicodeDecodeError, UnicodeEncodeError):
                self.fail("Link title has non-ASCII text:" + link.title)

    def test_undergrad_category(self):
        category_id = ResCategoryLink()._concat_id("Student & Campus Life")
        self.assertEquals(category_id, "studentcampuslife")
        affi = {"grad": False,
                "undergrad": True,
                "pce": False,
                "fyp": False}

        links = _get_links_by_category_and_campus(category_id,
                                                  "seattle",
                                                  affi)
        self.assertEquals(len(links), 22)

        links = _get_links_by_category_and_campus(category_id,
                                                  "bothell",
                                                  affi)
        self.assertEquals(len(links), 21)

        links = _get_links_by_category_and_campus(category_id,
                                                  "tacoma",
                                                  affi)
        self.assertEquals(len(links), 21)

    def test_grad_category(self):
        category_id = ResCategoryLink()._concat_id("Student & Campus Life")
        self.assertEquals(category_id, "studentcampuslife")
        affi = {"grad": True,
                "undergrad": False,
                "pce": False,
                "fyp": False}
        links = _get_links_by_category_and_campus(category_id,
                                                  "seattle",
                                                  affi)
        self.assertEquals(len(links), 24)

        links = _get_links_by_category_and_campus(category_id,
                                                  "bothell",
                                                  affi)
        self.assertEquals(len(links), 23)

        links = _get_links_by_category_and_campus(category_id,
                                                  "tacoma",
                                                  affi)
        self.assertEquals(len(links), 23)

    def test_pce_links(self):
        category_id = ResCategoryLink()._concat_id("Student & Campus Life")
        self.assertEquals(category_id, "studentcampuslife")
        affi = {"grad": False,
                "undergrad": False,
                "pce": True,
                "fyp": False}
        links = _get_links_by_category_and_campus(category_id,
                                                  "",
                                                  affi)
        self.assertEquals(len(links), 6)

    def test_fyp_links(self):
        category_id = ResCategoryLink()._concat_id("Student & Campus Life")
        self.assertEquals(category_id, "studentcampuslife")
        affi = {"grad": False,
                "undergrad": False,
                "pce": False,
                "fyp": True}
        links = _get_links_by_category_and_campus(category_id,
                                                  "",
                                                  affi)
        self.assertEquals(len(links), 7)

    def test_get_all_grouped(self):
        req = get_request_with_user("javerage")
        rl = Resource_Links(csv_filename="test/resource_link_import.csv")
        links = rl.get_all_grouped_links(req)
        self.assertEqual(len(links), 2)
        self.assertEqual(links[0]['category_id'], "academics")
        self.assertEqual(len(links[0]['subcategories']), 1)
        self.assertEqual(links[0]['subcategories']['A & T']['subcat_id'],
                         'academicsat')
