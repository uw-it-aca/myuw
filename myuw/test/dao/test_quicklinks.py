# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TransactionTestCase
from myuw.models import (
  HiddenLink, VisitedLinkNew, CustomLink, User)
from myuw.test import get_request_with_user
from myuw.dao.user import get_user_model
from myuw.dao.affiliation import get_all_affiliations
from myuw.dao.quicklinks import (
    get_quicklink_data, get_link_label,
    add_custom_link, delete_custom_link, edit_custom_link,
    add_hidden_link, delete_hidden_link, get_recent_link_by_id)

from myuw.test import get_request_with_user


class TestQuickLinkDAO(TransactionTestCase):

    def test_MUWM4955(self):
        username = 'none'
        req = get_request_with_user(username)
        user = get_user_model(req)

        u1 = add_custom_link(
            req, 'http://www.washington.edu/home/peopledir/',
            link_label="UW Directory")
        self.assertEqual(u1.url,  'http://www.washington.edu/home/peopledir/')

        v1 = VisitedLinkNew.objects.create(
            user=user, url=u1.url, label=u1.label)
        self.assertTrue(get_recent_link_by_id(req, v1.pk))

        h1 = HiddenLink.objects.create(
            user=user, url="https://uwnetid.washington.edu/manage/"
        )

        data = get_quicklink_data(req)
        self.maxDiff = None
        self.assertEqual(len(data), 3)
        self.assertEqual(len(data["custom_links"]), 1)
        self.assertEqual(data["custom_links"][0]['url'], u1.url)
        self.assertEqual(data["custom_links"][0]['label'], u1.label)

        self.assertEqual(len(data["default_links"]), 3)

        self.assertEqual(len(data["recent_links"]), 1)
        self.assertEqual(data["recent_links"][0]['url'], v1.url)
        self.assertTrue(data["recent_links"][0]['added'])

    def test_link_label_override(self):
        req = get_request_with_user('none')
        user = get_user_model(req)
        data = {"user": user,
                "url": "http://example.com?q=replaceit",
                "label": "Original"}

        l1 = VisitedLinkNew.objects.create(**data)

        self.assertEqual(get_link_label(l1), "Row For Unit Tests")

        l1 = VisitedLinkNew.objects.create(user=user,
                                           url="http://example.com?q=whatever",
                                           label="Original")
        self.assertEqual(get_link_label(l1), "Original")

    def test_hidden_link(self):
        req = get_request_with_user('none')
        url = "http://s.ss.edu"
        link = add_hidden_link(req, url)
        self.assertEqual(link.url, url)
        # second time
        link1 = add_hidden_link(req, url)
        self.assertEqual(link.pk, link1.pk)

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
        self.assertEqual(link1.url, url)
        self.assertEqual(link1.label, link_label)
        # second time
        link2 = add_custom_link(req, url, link_label)
        self.assertEqual(link2.pk, link1.pk)

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
        self.assertEqual(link1.url, url1)

        url2 = "http://s2.ss.edu"
        label2 = "s2"
        link2 = edit_custom_link(req, link1.pk, url2, label2)
        self.assertIsNotNone(link2)
        self.assertEqual(link2.label, label2)

    def test_get_quicklink_data(self):
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

        self.assertEqual(qls['default_links'][11]['label'],
                         "International Student Services (ISS)")

    def test_bot_quicklinks(self):
        username = "botgrad"
        req = get_request_with_user(username)
        bot_qls = get_quicklink_data(req)
        self.assertEqual(
            bot_qls["default_links"][9]["url"], "https://www.uwb.edu/cie")

    def test_tac_quicklinks(self):
        username = "tacgrad"
        req = get_request_with_user(username)
        tac_qls = get_quicklink_data(req)
        self.assertEqual(
            tac_qls["default_links"][11]["label"], "Online Learning Support")
