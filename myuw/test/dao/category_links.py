from django.test import TestCase
import datetime
from myuw.dao.category_links import _get_links_by_category_and_campus, \
    _get_category_id


class TestCategoryLinks(TestCase):

    def test_undergrad_category(self):
        category_id = _get_category_id("Student & Campus Life")
        self.assertEquals(category_id, "studentcampuslife")
        affi = {"grad": False,
                "undergrad": True,
                "pce": False}
        links = _get_links_by_category_and_campus(category_id,
                                                  "seattle",
                                                  affi)
        self.assertEquals(len(links), 24)

        links = _get_links_by_category_and_campus(category_id,
                                                  "bothell",
                                                  affi)
        self.assertEquals(len(links), 22)

        links = _get_links_by_category_and_campus(category_id,
                                                  "tacoma",
                                                  affi)
        self.assertEquals(len(links), 22)

    def test_grad_category(self):
        category_id = _get_category_id("Student & Campus Life")
        self.assertEquals(category_id, "studentcampuslife")
        affi = {"grad": True,
                "undergrad": False,
                "pce": False}
        links = _get_links_by_category_and_campus(category_id,
                                                  "seattle",
                                                  affi)
        self.assertEquals(len(links), 26)

        links = _get_links_by_category_and_campus(category_id,
                                                  "bothell",
                                                  affi)
        self.assertEquals(len(links), 24)

        links = _get_links_by_category_and_campus(category_id,
                                                  "tacoma",
                                                  affi)
        self.assertEquals(len(links), 24)

    def test_pce_links(self):
        category_id = _get_category_id("Student & Campus Life")
        self.assertEquals(category_id, "studentcampuslife")
        affi = {"grad": False,
                "undergrad": False,
                "pce": True}
        links = _get_links_by_category_and_campus(category_id,
                                                  "",
                                                  affi)
        self.assertEquals(len(links), 5)
