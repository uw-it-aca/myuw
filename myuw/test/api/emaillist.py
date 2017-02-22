import json
from django.core.urlresolvers import reverse
from django.test import Client
from django.test.utils import override_settings
from myuw.views.api.emaillist import Emaillist
from myuw.test import get_request, get_request_with_user, get_user
from myuw.test.api import MyuwApiTest, require_url,\
    fdao_sws_override, fdao_mailman_override


EMAILBACKEND = 'django.core.mail.backends.locmem.EmailBackend'
email_backend_override = override_settings(EMAIL_BACKEND=EMAILBACKEND)


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

    def test_post_wo_csrf_check(self):
        with self.settings(EMAIL_HOST='app.some.edu',
                           EMAIL_PORT=21,
                           EMAIL_USE_TLS=False,
                           MAILMAN_COURSEREQUEST_RECIPIENT='dummy@uw.edu'):
            client = Client()
            get_user('billsea')
            client.login(username='billsea', password='pass')
            url = reverse("myuw_emaillist_api")
            resp = client.post(
                url,
                {u'section_single_A': u'2013,spring,PHYS,122/A',
                 u'secondary_single_AA': u'2013,spring,PHYS,122/AA',
                 u'secondary_single_AB': u'2013,spring,PHYS,122/AB',
                 u'secondary_single_AC': u'2013,spring,PHYS,122/AC',
                 u'secondary_single_AD': u'2013,spring,PHYS,122/AD',
                 u'secondary_single_AS': u'2013,spring,PHYS,122/AS',
                 })
            self.assertEquals(resp.status_code, 200)
            self.assertEquals(json.loads(resp.content),
                              {'request_sent': True,
                               'total_lists_requested': 6})

            resp = client.post(
                url, {u'csrfmiddlewaretoken': [u'54qLUQ5ER737oHxECBuMGP']})
            self.assertEquals(resp.status_code, 200)
            self.assertEquals(json.loads(resp.content),
                              {'none_selected': True})
            resp = client.post(url,
                               {u'section_single_A': u'2013,spring,PHYS,122,A',
                                u'section_single': u'2013,spring,PHYS,122/A'})
            self.assertEquals(resp.status_code, 400)

    def test_not_instructor_post(self):
        client = Client()
        get_user('none')
        client.login(username='none', password='pass')
        url = reverse("myuw_emaillist_api")
        resp = client.post(
            url,
            {u'section_single_A': u'2013,spring,PHYS,122/A',
             u'secondary_single_AA': u'2013,spring,PHYS,122/AA'})
        self.assertEquals(resp.status_code, 403)
        self.assertEquals(resp.content,
                          'Access Forbidden to Non Instructor')
