# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.utils import timezone
from datetime import datetime, timedelta
from myuw.dao.user import get_user_model
from myuw.models import VisitedLinkNew
from myuw.test import get_request_with_user
from myuw.test.api import MyuwApiTest

TEST_URLS = ('http://google.com', 'http://uw.edu', 'http://cs.uw.edu')


class TestLink(MyuwApiTest):
    def test_user_recent_basic(self):
        req = get_request_with_user('none')
        user = get_user_model(req)
        for url in TEST_URLS:
            VisitedLinkNew.objects.create(user=user,
                                          url=url)

        recent = VisitedLinkNew.recent_for_user(user)
        self.assertEquals(len(recent), 3)
        self.assertEquals(recent[0].url, TEST_URLS[2])
        self.assertEquals(recent[1].url, TEST_URLS[1])
        self.assertEquals(recent[2].url, TEST_URLS[0])

    def test_user_recent_multi_visit(self):
        req = get_request_with_user('none')
        user = get_user_model(req)
        for url in TEST_URLS:
            for i in range(3):
                VisitedLinkNew.objects.create(user=user,
                                              url=url)

        recent = VisitedLinkNew.recent_for_user(user)
        self.assertEquals(len(recent), 3)
        self.assertEquals(recent[0].url, TEST_URLS[2])
        self.assertEquals(recent[1].url, TEST_URLS[1])
        self.assertEquals(recent[2].url, TEST_URLS[0])

    def test_max_old_links(self):
        req = get_request_with_user('none')
        user = get_user_model(req)
        VisitedLinkNew.objects.create(user=user, url=TEST_URLS[0])
        for i in range(VisitedLinkNew.MAX_RECENT_HISTORY):
            VisitedLinkNew.objects.create(user=user, url=TEST_URLS[1])
        VisitedLinkNew.objects.create(user=user, url=TEST_URLS[2])

        recent = VisitedLinkNew.recent_for_user(user)
        self.assertEquals(len(recent), 2)
        self.assertEquals(recent[0].url, TEST_URLS[2])
        self.assertEquals(recent[1].url, TEST_URLS[1])

    def test_max_by_date(self):
        req = get_request_with_user('none')
        user = get_user_model(req)
        visit_date = (timezone.now() +
                      VisitedLinkNew.OLDEST_RECENT_TIME_DELTA +
                      timedelta(seconds=-1))

        o = VisitedLinkNew.objects.create(user=user, url=TEST_URLS[0])
        o.visit_date = visit_date
        o.save()

        VisitedLinkNew.objects.create(user=user, url=TEST_URLS[1])
        recent = VisitedLinkNew.recent_for_user(user)
        self.assertEquals(len(recent), 1)
        self.assertEquals(recent[0].url, TEST_URLS[1])

    def test_none(self):
        req = get_request_with_user('none')
        user = get_user_model(req)
        recent = VisitedLinkNew.recent_for_user(user)
        self.assertEquals(recent, [])

    def test_popular(self):
        req1 = get_request_with_user('none')
        user1 = get_user_model(req1)

        req2 = get_request_with_user('none1')
        user2 = get_user_model(req2)

        VisitedLinkNew.objects.create(user=user1, url=TEST_URLS[0],
                                      is_student=True, is_seattle=True)

        VisitedLinkNew.objects.create(user=user2, url=TEST_URLS[0],
                                      is_seattle=True)
        VisitedLinkNew.objects.create(user=user2, url=TEST_URLS[1])
        VisitedLinkNew.objects.create(user=user2, url=TEST_URLS[2],
                                      is_seattle=True)

        popular_links = VisitedLinkNew.get_popular()

        self.assertEquals(len(popular_links), 3)
        self.assertEquals(popular_links[0]['url'], TEST_URLS[0])
        self.assertEquals(popular_links[0]['popularity'], 4)

        self.assertEquals(popular_links[1]['url'], TEST_URLS[2])
        self.assertEquals(popular_links[1]['popularity'], 1)

        self.assertEquals(popular_links[2]['url'], TEST_URLS[1])
        self.assertEquals(popular_links[2]['popularity'], 1)

        popular_links = VisitedLinkNew.get_popular(is_student=True)
        self.assertEquals(len(popular_links), 1)
        self.assertEquals(popular_links[0]['url'], TEST_URLS[0])
        self.assertEquals(popular_links[0]['popularity'], 1)

        popular_links = VisitedLinkNew.get_popular(is_seattle=True)
        self.assertEquals(len(popular_links), 2)
        self.assertEquals(popular_links[0]['url'], TEST_URLS[0])
        self.assertEquals(popular_links[0]['popularity'], 4)
        self.assertEquals(popular_links[1]['url'], TEST_URLS[2])
        self.assertEquals(popular_links[1]['popularity'], 1)

    def test_popular_multi_labels(self):
        req1 = get_request_with_user('none')
        user1 = get_user_model(req1)
        req2 = get_request_with_user('none1')
        user2 = get_user_model(req2)
        req3 = get_request_with_user('none2')
        user3 = get_user_model(req3)

        VisitedLinkNew.objects.create(user=user1, url=TEST_URLS[0], label="x",
                                      is_student=True, is_seattle=True)
        VisitedLinkNew.objects.create(user=user2, url=TEST_URLS[0], label="x",
                                      is_seattle=True)
        VisitedLinkNew.objects.create(user=user2, url=TEST_URLS[0], label=None,
                                      is_seattle=True)
        VisitedLinkNew.objects.create(user=user3, url=TEST_URLS[0], label=None,
                                      is_seattle=True)

        VisitedLinkNew.objects.create(user=user1, url=TEST_URLS[1], label=None,
                                      is_student=True, is_seattle=True)
        VisitedLinkNew.objects.create(user=user2, url=TEST_URLS[1], label="x",
                                      is_seattle=True)
        VisitedLinkNew.objects.create(user=user3, url=TEST_URLS[1], label="y",
                                      is_seattle=True)

        popular_links = VisitedLinkNew.get_popular()
        self.assertEquals(len(popular_links), 2)
        self.assertEquals(popular_links[0]['url'], TEST_URLS[0])
        self.assertEquals(popular_links[0]['popularity'], 16)
        self.assertEquals(popular_links[0]['labels'], ['', 'x'])

        self.assertEquals(popular_links[1]['url'], TEST_URLS[1])
        self.assertEquals(popular_links[1]['popularity'], 9)
        self.assertEquals(popular_links[1]['labels'], ['', 'x', 'y'])
