from unittest2 import TestCase
from myuw.models import VisitedLink, CustomLink, PopularLink, User
from myuw.dao.quicklinks import get_quicklink_data, get_link_label
from myuw.test import get_request_with_user


class TestQuickLinkDAO(TestCase):
    def test_recent_filtering(self):
        def _get_recent(data):
            recent = set()
            for link in data['recent_links']:
                recent.add(link['url'])
            return recent

        VisitedLink.objects.all().delete()
        PopularLink.objects.all().delete()
        CustomLink.objects.all().delete()
        username = 'link_dao_user'
        get_request_with_user(username)
        user, created = User.objects.get_or_create(uwnetid=username)

        u1 = 'http://example.com?q=1'
        u2 = 'http://example.com?q=2'

        v1 = VisitedLink.objects.create(username=username, url=u1)

        v2 = VisitedLink.objects.create(username=username, url=u2)

        data = get_quicklink_data({})
        recent = _get_recent(data)

        self.assertEquals(len(recent), 2)
        self.assertTrue(u1 in recent)
        self.assertTrue(u2 in recent)

        PopularLink.objects.create(url=u2)

        data = get_quicklink_data({})
        recent = _get_recent(data)

        self.assertEquals(len(recent), 1)
        self.assertTrue(u1 in recent)

        CustomLink.objects.create(user=user, url=u1)
        data = get_quicklink_data({})
        recent = _get_recent(data)

        self.assertEquals(len(recent), 0)

        for i in range(10):
            VisitedLink.objects.create(username=username,
                                       url="http://example.com?q=%s" % i)

        data = get_quicklink_data({})
        recent = _get_recent(data)

        self.assertEquals(len(recent), 5)

    def test_link_label_override(self):
        username = 'ql_override_label_user'
        l1 = VisitedLink.objects.create(username=username,
                                        url="http://example.com?q=replaceit",
                                        label="Original")

        self.assertEquals(get_link_label(l1), "Row For Unit Tests")

        l1 = VisitedLink.objects.create(username=username,
                                        url="http://example.com?q=whatever",
                                        label="Original")
        self.assertEquals(get_link_label(l1), "Original")
