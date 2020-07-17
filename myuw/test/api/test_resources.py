import json
from django.urls import reverse
from myuw.dao.user import get_user_model
from myuw.models import ResourceCategoryPin
from myuw.test import get_request_with_user
from myuw.test.api import MyuwApiTest


class TestResources(MyuwApiTest):

    def test_get_resources_list(self):
        self.set_user('javerage')
        url = reverse('myuw_resources_api')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 9)
        self.assertEqual(data[1]["category_id"],
                         "emailandaccountsandidentity")
        self.assertEqual(data[2]["category_id"],
                         "servicesforfacultyandstaff")

    def test_pin_resource(self):
        self.set_user('bill')
        url = reverse('myuw_resources_pin_api',
                      kwargs={'category_id': 'teachingtools'})
        response = self.client.post(
            url, content_type='application_json')
        self.assertEqual(response.status_code, 200)

        categories = ResourceCategoryPin.objects.all()
        self.assertEqual(len(categories), 1)
        self.assertEqual(categories[0].resource_category_id, 'teachingtools')

        response = self.client.delete(
            url, content_type='application_json')
        self.assertEqual(response.status_code, 200)
        categories = ResourceCategoryPin.objects.all()
        self.assertEqual(len(categories), 0)

    def test_disable_action(self):
        with self.settings(DEBUG=False,
                           MYUW_DISABLE_ACTIONS_WHEN_OVERRIDE=True):
            self.set_user('javerage')
            self.set_userservice_override('bill')

            url = reverse('myuw_resources_pin_api',
                          kwargs={'category_id': 'teachinginclasstools'})
            response = self.client.post(
                url, content_type='application_json')
            self.assertEqual(response.status_code, 403)

            url = reverse('myuw_resources_pin_api',
                          kwargs={'category_id': 'teachinginclasstools'})
            response = self.client.delete(
                url, content_type='application_json')
            self.assertEqual(response.status_code, 403)
