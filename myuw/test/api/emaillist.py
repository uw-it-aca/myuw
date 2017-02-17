import json
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
