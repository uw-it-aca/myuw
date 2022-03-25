# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from myuw.test.dao.test_persistent_messages import setup_db, set_tags
from myuw.test.api import MyuwApiTest, require_url


@fdao_mylib_override
@require_url('myuw_persistent_messages')
class TestPersistentMsgApi(MyuwApiTest):
    fixtures = ['persistent_messages.json']

    def get_response(self):
        return self.get_response_by_reverse('myuw_persistent_messages')

    def test_javerage(self):
        self.set_user('javerage')
        msg = setup_db(self.request)
        msg = set_tags(msg, ['seattle', 'undergraduate'])

        response = self.get_response()
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEquals(
            data[0],
            {'content': 'Hello World!',
             'end': None,
             'id': 1,
             'level': 20,
             'level_name': 'Info',
             'seattle': True,
             'start ': '2013-04-14T00:00:01-07:00',
             'undergraduate': True})
