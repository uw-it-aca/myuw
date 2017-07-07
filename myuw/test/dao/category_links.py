from django.test import TestCase
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from myuw.dao.category_links import _get_links_by_category_and_campus, \
    _get_category_id, Res_Links
import re


class TestCategoryLinks(TestCase):

    def test_get_all_likes(self):
        all_links = Res_Links.get_all_links()
        self.assertEquals(len(all_links), 155)
        val = URLValidator()
        for link in all_links:
            try:
                link.url.decode('ascii')
            except UnicodeDecodeError:
                self.fail("%s url has non-ASCII text: %s" %
                          (link.title, link.url))

            try:
                val(link.url)
            except ValidationError:
                # allow relative references
                if not re.match('^/[\w/]+$', link.url):
                    self.fail("Invalid url:" + link.url)

            try:
                link.title.decode('ascii')
            except UnicodeDecodeError:
                self.fail("Link title has non-ASCII text:" + link.title)

    def test_undergrad_category(self):
        category_id = _get_category_id("Student & Campus Life")
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
        category_id = _get_category_id("Student & Campus Life")
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
        category_id = _get_category_id("Student & Campus Life")
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
        category_id = _get_category_id("Student & Campus Life")
        self.assertEquals(category_id, "studentcampuslife")
        affi = {"grad": False,
                "undergrad": False,
                "pce": False,
                "fyp": True}
        links = _get_links_by_category_and_campus(category_id,
                                                  "",
                                                  affi)
        self.assertEquals(len(links), 7)
