from django.test import TransactionTestCase
from myuw.models import VisitedLinkNew, CustomLink, PopularLink, User
from myuw.test import get_request_with_user, get_myuw_user
from myuw.dao.quicklinks import get_quicklink_data, get_link_label,\
    add_custom_link, delete_custom_link, edit_custom_link,\
    add_hidden_link, delete_hidden_link, get_popular_link_by_id,\
    get_recent_link_by_id

from myuw.test import get_request_with_user


class TestQuickLinkDAO(TransactionTestCase):

    def test_recent_filtering(self):
        def _get_recent(data):
            recent = set()
            for link in data['recent_links']:
                recent.add(link['url'])
            return recent

        username = 'link_dao_user'
        get_request_with_user(username)
        user, created = User.objects.get_or_create(uwnetid=username)

        u1 = 'http://example.com?q=1'
        u2 = 'http://example.com?q=2'

        v1 = VisitedLinkNew.objects.create(user=user, url=u1)
        self.assertTrue(get_recent_link_by_id(v1.pk))

        v2 = VisitedLinkNew.objects.create(user=user, url=u2)

        data = get_quicklink_data({})
        recent = _get_recent(data)

        self.assertEquals(len(recent), 2)
        self.assertTrue(u1 in recent)
        self.assertTrue(u2 in recent)

        plink = PopularLink.objects.create(url=u2)
        self.assertTrue(get_popular_link_by_id(plink.pk))

        data = get_quicklink_data({})
        recent = _get_recent(data)

        self.assertEquals(len(recent), 1)
        self.assertTrue(u1 in recent)

        CustomLink.objects.create(user=user, url=u1)
        data = get_quicklink_data({})
        recent = _get_recent(data)

        self.assertEquals(len(recent), 0)

        for i in range(10):
            VisitedLinkNew.objects.create(user=user,
                                          url="http://example.com?q=%s" % i)

        data = get_quicklink_data({})
        recent = _get_recent(data)

        self.assertEquals(len(recent), 5)

    def test_link_label_override(self):
        username = 'ql_override_lbl_user'
        user = get_myuw_user(username)
        data = {"user": user,
                "url": "http://example.com?q=replaceit",
                "label": "Original"}

        l1 = VisitedLinkNew.objects.create(**data)

        self.assertEquals(get_link_label(l1), "Row For Unit Tests")

        l1 = VisitedLinkNew.objects.create(user=user,
                                           url="http://example.com?q=whatever",
                                           label="Original")
        self.assertEquals(get_link_label(l1), "Original")

    def test_hidden_link(self):
        username = 'add_hidlink_user'
        get_request_with_user(username)
        url = "http://s.ss.edu"
        link = add_hidden_link(url)
        self.assertEquals(link.url, url)
        # second time
        link1 = add_hidden_link(url)
        self.assertEquals(link.pk, link1.pk)

        self.assertIsNotNone(delete_hidden_link(link.pk))
        # second time
        self.assertIsNone(delete_hidden_link(link.pk))

    def test_add_custom_link(self):
        username = 'add_link_user'
        get_request_with_user(username)
        link = add_custom_link("http://s1.ss.edu")
        self.assertIsNone(link.label)

        url = "http://s.ss.edu"
        link_label = "ss"
        link1 = add_custom_link(url, link_label)
        self.assertEquals(link1.url, url)
        self.assertEquals(link1.label, link_label)
        # second time
        link2 = add_custom_link(url, link_label)
        self.assertEquals(link2.pk, link1.pk)

    def test_delete_custom_link(self):
        username = 'rm_link_user'
        get_request_with_user(username)
        url = "http://s.ss.edu"
        link = add_custom_link(url)
        self.assertIsNotNone(delete_custom_link(link.pk))
        # second time
        self.assertIsNone(delete_custom_link(link.pk))

    def test_edit_custom_link(self):
        username = 'edit_link_user'
        get_request_with_user(username)
        url = "http://s.ss.edu"
        link = add_custom_link(url)

        url1 = "http://s1.ss.edu"
        link1 = edit_custom_link(link.pk, url1)
        self.assertEquals(link1.url, url1)

        url2 = "http://s2.ss.edu"
        label2 = "s2"
        link2 = edit_custom_link(link1.pk, url2, label2)
        self.assertIsNotNone(link2)
        self.assertEquals(link2.label, label2)
