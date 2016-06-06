from myuw.test.api import MyuwApiTest, require_url
import json


@require_url('myuw_home')
class TestLinks(MyuwApiTest):

    def test_academics_links(self):
        self.set_user('javerage')
        response = self.get_response_by_reverse(
            'myuw_links_api',
            kwargs={'category_id': 'academics'})
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(data["link_data"][0]["subcategory"], "Registration")
        self.assertGreater(len(data["link_data"][0]["links"]), 1)
