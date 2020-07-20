from django.test import TransactionTestCase
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from myuw.dao.category_links import _get_links_by_category_and_campus, \
    Res_Links, Resource_Links, pin_category, delete_categor_pin
from myuw.dao.exceptions import InvalidResourceCategory
from myuw.models.res_category_link import ResCategoryLink
from myuw.test import get_request_with_user
import re


class TestCategoryLinks(TransactionTestCase):

    def _test_ascii(self, s):
        s.encode('ascii')  # python 3

    def test_get_all_links(self):
        all_links = Res_Links.get_all_links()
        self.assertEquals(len(all_links), 56)
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
        self.assertEquals(len(links), 0)

        links = _get_links_by_category_and_campus(category_id,
                                                  "bothell",
                                                  affi)
        self.assertEquals(len(links), 0)

        links = _get_links_by_category_and_campus(category_id,
                                                  "tacoma",
                                                  affi)
        self.assertEquals(len(links), 0)

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
        self.assertEquals(len(links), 0)

        links = _get_links_by_category_and_campus(category_id,
                                                  "bothell",
                                                  affi)
        self.assertEquals(len(links), 0)

        links = _get_links_by_category_and_campus(category_id,
                                                  "tacoma",
                                                  affi)
        self.assertEquals(len(links), 0)

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
        self.assertEquals(len(links), 0)

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
        self.assertEquals(len(links), 0)

    def test_get_all_grouped(self):
        req = get_request_with_user("javerage")
        rl = Resource_Links(csv_filename="test/resource_link_import.csv")
        links = rl.get_all_grouped_links(req)
        self.assertEqual(len(links), 2)
        self.assertEqual(links[0]['category_id'], "academics")
        self.assertEqual(len(links[0]['subcategories']), 1)
        self.assertEqual(links[0]['subcategories']['A & T']['subcat_id'],
                         'academicsat')

    def test_category_exists(self):
        req = get_request_with_user("javerage")
        rl = Resource_Links(csv_filename="test/resource_link_import.csv")
        self.assertFalse(rl.category_exists("foobar"))
        self.assertTrue(rl.category_exists("academicsat"))

    def test_category_pin(self):
        req = get_request_with_user('javerage')

        rl = Resource_Links()
        pinned = rl.get_pinned_links(req)
        self.assertEqual(len(pinned), 0)

        pin_category(req, "academicsadvisingtutoring")
        pinned = rl.get_pinned_links(req)
        self.assertEqual(len(pinned), 1)

        delete_categor_pin(req, "academicsadvisingtutoring")
        pinned = rl.get_pinned_links(req)
        self.assertEqual(len(pinned), 0)

        with self.assertRaises(InvalidResourceCategory):
            pin_category(req, 'foobar')

    def test_staff_links(self):
        req = get_request_with_user('bill')
        links = Resource_Links().get_all_grouped_links(req)
        self.assertEqual(len(links), 9)
        self.assertEqual(links[8]['category_name'], 'Teaching')
        self.assertEqual(len(links[8]['subcategories']), 4)
        self.assertEqual(len(links[8]['subcategories']['Tools']), 5)
        self.assertEqual(
            links[8]['subcategories']['Tools']['links'][4]['title'],
            'Course stats')
        self.assertEqual(
            links[8]['subcategories']['Tools']['links'][5]['title'], 'Zoom')

        req = get_request_with_user('billbot')
        links = Resource_Links().get_all_grouped_links(req)
        self.assertEqual(len(links), 9)
        self.assertEqual(links[2]['category_name'],
                         'Services for Faculty and Staff')
        req = get_request_with_user('billtac')
        links = Resource_Links().get_all_grouped_links(req)
        self.assertEqual(len(links), 9)
        self.assertEqual(links[2]['category_name'],
                         'Services for Faculty and Staff')
