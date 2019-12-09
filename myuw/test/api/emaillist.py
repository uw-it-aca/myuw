import json
from django.urls import reverse
from django.test import Client
from django.test.utils import override_settings
from userservice.user import UserService
from myuw.views.api.emaillist import (
    section_id_matched, is_emaillist_authorized)
from myuw.test import get_request, get_request_with_user, get_user,\
    email_backend_override, set_override_user
from myuw.test.api import MyuwApiTest, require_url,\
    fdao_sws_override, fdao_mailman_override, VALIDATE, OVERRIDE


@email_backend_override
@fdao_mailman_override
@fdao_sws_override
@require_url('myuw_home')
class TestEmaillistApi(MyuwApiTest):

    def test_get_err(self):
        self.set_user('none')
        response = self.get_response_by_reverse(
            'myuw_emaillist_api',
            kwargs={'year': 2013,
                    'quarter': 'spring',
                    'curriculum_abbr': 'PHYS',
                    'course_number': '121',
                    'section_id': 'A'})
        self.assertEquals(response.status_code, 403)

    def test_get(self):
        self.set_user('bill')
        response = self.get_response_by_reverse(
            'myuw_emaillist_api',
            kwargs={'year': 2013,
                    'quarter': 'spring',
                    'curriculum_abbr': 'PHYS',
                    'course_number': '121',
                    'section_id': 'A'})
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)

        self.assertEquals(data['year'], 2013)
        self.assertEquals(data['quarter'], 'spring')
        self.assertTrue(data["has_multiple_sections"])
        self.assertTrue(data["is_primary"])
        self.assertEquals(data["section_list"]["list_address"],
                          "phys121a_sp13")
        self.assertEquals(data["secondary_combined_list"]["list_address"],
                          "multi_phys121a_sp13")
        self.assertEquals(len(data["secondary_section_lists"]), 21)
        self.assertEquals(data["course_number"], "121")
        self.assertEquals(data["course_abbr"], "PHYS")
        self.assertEquals(data["section_id"], "A")
        self.assertTrue(data["has_lists"])

    def test_get_bot(self):
        self.set_user('billbot')
        response = self.get_response_by_reverse(
            'myuw_emaillist_api',
            kwargs={'year': 2013,
                    'quarter': 'summer',
                    'curriculum_abbr': 'B%20BIO',
                    'course_number': '180',
                    'section_id': 'A'})
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data["is_primary"])

    def test_post_with_csrf_checks(self):
        client = Client(enforce_csrf_checks=True)
        get_user('billsea')
        client.login(username='billsea', password='pass')
        url = reverse("myuw_emaillist_api")
        resp = client.post(
            url,
            {u'section_single_A': u'2013,spring,PHYS,122/A',
             u'secondary_single_AA': u'2013,spring,PHYS,122/AA',
             })
        self.assertEqual(resp.status_code, 403)

    def test_section_id_matched(self):
        self.assertTrue(section_id_matched(u'section_single_A',
                                           u'2013,spring,PHYS,122/A'))
        self.assertTrue(section_id_matched(u'section_single_AA',
                                           u'2013,spring,PHYS,122/AA'))
        self.assertFalse(section_id_matched(u'section_single_A', None))
        self.assertFalse(section_id_matched(u'section_single_B',
                                            u'2013,spring,PHYS,122/A'))
        self.assertFalse(section_id_matched(u'section_single_B',
                                            u'2013,spring,PHYS,122,A'))
        self.assertFalse(section_id_matched(u'single_A',
                                            u'2013,spring,PHYS,122/A'))

    def test_post_wo_csrf_check(self):
        with self.settings(MAILMAN_COURSEREQUEST_RECIPIENT='dummy@uw.edu'):
            self.set_user('billsea')

            url = reverse("myuw_emaillist_api")
            # resp = self.client.post(
            #     url,
            #     {u'section_single_A': u'2013,spring,PHYS,122/A',
            #      })
            # self.assertEquals(resp.status_code, 200)
            # self.assertEquals(json.loads(resp.content),
            #                   {'request_sent': True,
            #                    'total_lists_requested': 1})
            #
            # resp = self.client.post(
            #     url, {u'csrfmiddlewaretoken': [u'54qLUQ5ER737oHxECBuMGP']})
            # self.assertEquals(resp.status_code, 200)
            # self.assertEquals(json.loads(resp.content),
            #                   {'none_selected': True})
            resp = self.client.post(
                url,
                {u'section_single_A': u'2013,spring,PHYS,122,A',
                 u'section_single': u'2013,spring,PHYS,122/A'})
            self.assertEquals(resp.status_code, 400)

    def test_missing_section_post(self):
        self.set_user('billsea')
        url = reverse("myuw_emaillist_api")
        resp = self.client.post(
            url,
            {u'section_single_ZC': u'2013,spring,PHYS,122/ZC'})
        self.assertEquals(resp.status_code, 403)

        self.assertEquals(resp.content, b'Access Forbidden to Non Instructor')

    def test_not_instructor_post(self):
        self.set_user('billsea')
        url = reverse("myuw_emaillist_api")
        resp = self.client.post(
            url,
            {u'section_single_A': u'2013,spring,ESS,102/A'})
        self.assertEquals(resp.status_code, 403)

        self.assertEquals(resp.content, b'Access Forbidden to Non Instructor')

    def test_not_instructor_secondary_post(self):
        self.set_user('billsea')
        url = reverse("myuw_emaillist_api")
        resp = self.client.post(
            url,
            {u'section_single_AB': u'2013,spring,ESS,102/AB'})
        self.assertEquals(resp.status_code, 403)

        self.assertEquals(resp.content, b'Access Forbidden to Non Instructor')

    def test_primary_instructor_secondary_post(self):
        with self.settings(MAILMAN_COURSEREQUEST_RECIPIENT=""):
            self.set_user('bill')
            url = reverse("myuw_emaillist_api")
            resp = self.client.post(
                url,
                {u'section_single_AB': u'2013,spring,ESS,102/AB'})
            self.assertEquals(resp.status_code, 200)

    def test_override_primary_instructor_secondary_post(self):
        with self.settings(DEBUG=False,
                           MYUW_DISABLE_ACTIONS_WHEN_OVERRIDE=True,
                           MAILMAN_COURSEREQUEST_RECIPIENT="",
                           USERSERVICE_VALIDATION_MODULE=VALIDATE,
                           USERSERVICE_OVERRIDE_AUTH_MODULE=OVERRIDE):
            self.set_user('javerage')
            self.set_userservice_override("bill")
            self.assertEquals(UserService().get_override_user(), "bill")

            url = reverse("myuw_emaillist_api")
            resp = self.client.post(
                url,
                {u'section_single_AB': u'2013,spring,ESS,102/AB'})
            self.assertEquals(resp.status_code, 401)

    def test_is_emaillist_authorized(self):
        req = get_request_with_user('billbot')
        self.assertTrue(is_emaillist_authorized(req,
                                                "2013,summer,B BIO,180/A"))
        self.assertFalse(is_emaillist_authorized(req,
                                                 "2013,summer,B%20BIO,180/A"))
