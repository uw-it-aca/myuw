import json
from myuw.test.api import MyuwApiTest, require_url


@require_url('myuw_thrive_api')
class TestApiThrive(MyuwApiTest):

    def get_thrive_response(self):
        return self.get_response_by_reverse('myuw_thrive_api')

    def test_jnew_thrive(self):
        self.set_user('jnew')
        self.set_date('2013-09-28')
        response = self.get_thrive_response()
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data["week_label"], "Week 1")
        self.assertEquals(data["title"], "All the Time in the World?")

        self.set_date('2015-02-12')
        response = self.get_thrive_response()
        self.assertEquals(response.status_code, 404)

        self.set_date('2015-02-21')
        response = self.get_thrive_response()
        self.assertEquals(response.status_code, 404)
