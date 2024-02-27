# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from persistent_message.models import Message
from myuw.test.api import MyuwApiTest, require_url


@require_url('myuw_banner_message')
class PersistentMessageAPITest(MyuwApiTest):
    fixtures = ['persistent_messages.json']

    def get_response(self):
        return self.get_response_by_reverse('myuw_banner_message')

    def test_javerage(self):
        self.set_user('javerage')
        response = self.get_response()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)

        Message.objects.all().delete()
        response = self.get_response()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 0)
