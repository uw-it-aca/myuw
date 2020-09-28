from django.test import TransactionTestCase
from myuw.models import VisitedLinkNew, CustomLink, PopularLink, User
from myuw.test import get_request_with_user
from myuw.dao.user import get_user_model
from myuw.dao.affiliation import get_all_affiliations
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

        username = 'none'
        req = get_request_with_user(username)
        user = get_user_model(req)

        u1 = 'http://example.com?q=1'
        u2 = 'http://example.com?q=2'

        v1 = VisitedLinkNew.objects.create(user=user, url=u1)
        self.assertTrue(get_recent_link_by_id(req, v1.pk))

        v2 = VisitedLinkNew.objects.create(user=user, url=u2)

        data = get_quicklink_data(req)
        recent = _get_recent(data)

        self.assertEquals(len(recent), 2)
        self.assertTrue(u1 in recent)
        self.assertTrue(u2 in recent)

        plink = PopularLink.objects.create(url=u2)
        self.assertTrue(get_popular_link_by_id(plink.pk))
        self.assertIsNotNone(plink.json_data())
        self.assertIsNotNone(str(plink))

        data = get_quicklink_data(req)
        recent = _get_recent(data)

        self.assertEquals(len(recent), 1)
        self.assertTrue(u1 in recent)

        CustomLink.objects.create(user=user, url=u1)
        data = get_quicklink_data(req)
        recent = _get_recent(data)

        self.assertEquals(len(recent), 0)

        for i in range(10):
            VisitedLinkNew.objects.create(user=user,
                                          url="http://example.com?q=%s" % i)

        data = get_quicklink_data(req)
        recent = _get_recent(data)

        self.assertEquals(len(recent), 5)

    def test_link_label_override(self):
        req = get_request_with_user('none')
        user = get_user_model(req)
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
        req = get_request_with_user('none')
        url = "http://s.ss.edu"
        link = add_hidden_link(req, url)
        self.assertEquals(link.url, url)
        # second time
        link1 = add_hidden_link(req, url)
        self.assertEquals(link.pk, link1.pk)

        self.assertIsNotNone(delete_hidden_link(req, link.pk))
        # second time
        self.assertIsNone(delete_hidden_link(req, link.pk))

    def test_add_custom_link(self):
        username = 'none'
        req = get_request_with_user(username)
        link = add_custom_link(req, "http://s1.ss.edu")
        self.assertIsNone(link.label)

        url = "http://s.ss.edu"
        link_label = "ss"
        link1 = add_custom_link(req, url, link_label)
        self.assertEquals(link1.url, url)
        self.assertEquals(link1.label, link_label)
        # second time
        link2 = add_custom_link(req, url, link_label)
        self.assertEquals(link2.pk, link1.pk)

    def test_delete_custom_link(self):
        username = 'none'
        req = get_request_with_user(username)
        url = "http://s.ss.edu"
        link = add_custom_link(req, url)
        self.assertIsNotNone(delete_custom_link(req, link.pk))
        # second time
        self.assertIsNone(delete_custom_link(req, link.pk))

    def test_edit_custom_link(self):
        username = 'none'
        req = get_request_with_user(username)
        url = "http://s.ss.edu"
        link = add_custom_link(req, url)

        url1 = "http://s1.ss.edu"
        link1 = edit_custom_link(req, link.pk, url1)
        self.assertEquals(link1.url, url1)

        url2 = "http://s2.ss.edu"
        label2 = "s2"
        link2 = edit_custom_link(req, link1.pk, url2, label2)
        self.assertIsNotNone(link2)
        self.assertEquals(link2.label, label2)

    def test_get_quicklink_data(self):
        data = {
            "affiliation": "student",
            "url": "http://iss1.washington.edu/",
            "label": "ISS1",
            "campus": "seattle",
            "pce": False,
            "affiliation": "{intl_stud: True}",
            }
        plink = PopularLink.objects.create(**data)

        username = "jinter"
        req = get_request_with_user(username)
        affiliations = get_all_affiliations(req)
        user = get_user_model(req)
        link_data = {
            "user": user,
            "url": "http://iss.washington.edu/",
            "label": "ISS1",
            "is_anonymous": False,
            "is_student": affiliations.get('student', False),
            "is_undegrad": affiliations.get('undergrad', False),
            "is_grad_student": affiliations.get('grad', False),
            "is_employee": affiliations.get('employee', False),
            "is_faculty": affiliations.get('faculty', False),
            "is_seattle": affiliations.get('seattle', False),
            "is_tacoma": affiliations.get('tacoma', False),
            "is_bothell": affiliations.get('bothell', False),
            "is_pce": affiliations.get('pce', False),
            "is_student_employee": affiliations.get('stud_employee',
                                                    False),
            "is_intl_stud": affiliations.get('intl_stud', False)
        }
        l1 = VisitedLinkNew.objects.create(**link_data)

        qls = get_quicklink_data(req)
        self.assertEqual(qls['recent_links'][0]['label'], "ISS1")

        self.assertEqual(qls['default_links'][0]['label'],
                         "International Student Services (ISS)")

    def test_bot_quicklinks(self):
        username = "botgrad"
        req = get_request_with_user(username)
        bot_qls = get_quicklink_data(req)
        self.assertEqual(bot_qls['default_links'][0]['url'],
                         "http://www.uwb.edu/cie")

    def test_tac_quicklinks(self):
        username = "tacgrad"
        req = get_request_with_user(username)
        tac_qls = get_quicklink_data(req)
        self.assertEqual(tac_qls['default_links'][0]['label'],
                         "International Student and Scholar Services (ISSS)")

    def test_MUWM_4760(self):
        req = get_request_with_user('bill')
        data = get_quicklink_data(req)
        self.assertTrue(data['instructor'])
        self.assertTrue(data['sea_emp'])
        self.assertFalse(data['student'])

        req = get_request_with_user('javerage')
        data = get_quicklink_data(req)
        self.assertFalse(data['instructor'])
        self.assertTrue(data['student'])
        self.assertFalse(data['bot_student'])
        self.assertFalse(data['tac_student'])
        self.assertTrue(data['sea_student'])
        self.assertTrue(data['sea_emp'])
        self.assertFalse(data['bot_emp'])
        self.assertFalse(data['tac_emp'])

        req = get_request_with_user('jbothell')
        data = get_quicklink_data(req)
        self.assertTrue(data['student'])
        self.assertTrue(data['bot_student'])

        req = get_request_with_user('eight')
        data = get_quicklink_data(req)
        self.assertTrue(data['student'])
        self.assertTrue(data['tac_student'])
        self.assertTrue(data['instructor'])
        self.assertTrue(data['sea_emp'])
