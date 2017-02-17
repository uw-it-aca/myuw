import json
from myuw.views.api.emaillist import Emaillist
from myuw.test import get_request, get_request_with_user
from myuw.test.api import MyuwApiTest, require_url,\
    fdao_sws_override, fdao_mailman_override


@fdao_mailman_override
@fdao_sws_override
@require_url('myuw_home')
class TestEmaillistApi(MyuwApiTest):

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

    def test_post(self):
        now_request = get_request()
        get_request_with_user('billsea', now_request)
        now_request.POST = {
            u'section_single_A': [u'2013,spring,PHYS,122/A'],
            u'csrfmiddlewaretoken': [u'UHYAf4Kct0T']
            }
        resp = Emaillist().POST(now_request)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.content, '{"request_sent": true}')
