from django.test import TestCase
import datetime
from myuw.dao.category_links import _get_links_by_category_and_campus, \
    _get_category_id, Res_Links


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

    @staticmethod
    def validate_URL(url):
        return url.startswith('http')

    @staticmethod
    def validate_ascii(s):
        try:
            s.decode('ascii')
        except UnicodeDecodeError:
            return False

        return True

    def test_all_links_sanity(self):
        all_links = Res_Links.get_all_links()

        for link in all_links:
            strings = (
                link.url,
                link.title,
                link.category_name,
                link.sub_category,
            )
            for s in strings:
                if not(self.validate_ascii(s)):
                    self.fail(
                        'Found non-ASCII text %s in resource link %s'
                        % (s, link.title)
                    )

            if not(self.validate_URL(link.url)):
                self.fail(
                    'Expected URL, got "%s"' % link.url
                )
