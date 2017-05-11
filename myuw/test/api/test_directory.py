import json
from myuw.test.api import (MyuwApiTest, require_url, fdao_pws_override)


@fdao_pws_override
@require_url('myuw_directory_api')
class TestMyDirectoryInfo(MyuwApiTest):
    def get_directory_response(self, netid, adate=None):
        self.set_user(netid)
        return self.get_response_by_reverse('myuw_directory_api')

    def test_javerage(self):
        response = self.get_directory_response('javerage')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data['surname'], 'STUDENT')
        self.assertEquals(data['uwregid'], '9136CCB8F66711D5BE060004AC494FFE')

    def test_bill(self):
        response = self.get_directory_response('bill')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data['surname'], 'TEACHER')
        self.assertEquals(data['title1'], 'Associate Professor')
