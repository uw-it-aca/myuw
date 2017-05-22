from myuw.models import VisitedLink
from unittest2 import TestCase
from django.utils import timezone
from datetime import datetime, timedelta

TEST_URLS = ('http://google.com', 'http://uw.edu', 'http://cs.uw.edu')


class TestLink(TestCase):
    def test_user_recent_basic(self):
        VisitedLink.objects.all().delete()
        user = 'basic_recent'
        for url in TEST_URLS:
            VisitedLink.objects.create(username=user,
                                       url=url)

        recent = VisitedLink.recent_for_user(user)
        self.assertEquals(len(recent), 3)
        self.assertEquals(recent[0].url, TEST_URLS[2])
        self.assertEquals(recent[1].url, TEST_URLS[1])
        self.assertEquals(recent[2].url, TEST_URLS[0])

    def test_user_recent_multi_visit(self):
        VisitedLink.objects.all().delete()
        user = 'basic_recent'
        for url in TEST_URLS:
            for i in range(3):
                VisitedLink.objects.create(username=user,
                                           url=url)

        recent = VisitedLink.recent_for_user(user)
        self.assertEquals(len(recent), 3)
        self.assertEquals(recent[0].url, TEST_URLS[2])
        self.assertEquals(recent[1].url, TEST_URLS[1])
        self.assertEquals(recent[2].url, TEST_URLS[0])

    def test_max_old_links(self):
        VisitedLink.objects.all().delete()
        user = 'basic_recent'
        VisitedLink.objects.create(username=user, url=TEST_URLS[0])
        for i in range(VisitedLink.MAX_RECENT_HISTORY):
            VisitedLink.objects.create(username=user, url=TEST_URLS[1])
        VisitedLink.objects.create(username=user, url=TEST_URLS[2])

        recent = VisitedLink.recent_for_user(user)
        self.assertEquals(len(recent), 2)
        self.assertEquals(recent[0].url, TEST_URLS[2])
        self.assertEquals(recent[1].url, TEST_URLS[1])

    def test_max_by_date(self):
        VisitedLink.objects.all().delete()
        user = 'basic_recent'
        visit_date = (timezone.now() +
                      VisitedLink.OLDEST_RECENT_TIME_DELTA +
                      timedelta(seconds=-1))

        o = VisitedLink.objects.create(username=user, url=TEST_URLS[0])
        o.visit_date = visit_date
        o.save()

        VisitedLink.objects.create(username=user, url=TEST_URLS[1])
        recent = VisitedLink.recent_for_user(user)
        self.assertEquals(len(recent), 1)
        self.assertEquals(recent[0].url, TEST_URLS[1])

    def test_none(self):
        VisitedLink.objects.all().delete()
        user = 'basic_recent'
        recent = VisitedLink.recent_for_user(user)
        self.assertEquals(recent, [])

    def test_popular(self):
        VisitedLink.objects.all().delete()

        user1 = 'basic1'
        user2 = 'basic2'
        VisitedLink.objects.create(username=user1, url=TEST_URLS[0],
                                   is_student=True, is_seattle=True)
        VisitedLink.objects.create(username=user2, url=TEST_URLS[0],
                                   is_seattle=True)
        VisitedLink.objects.create(username=user2, url=TEST_URLS[1])
        VisitedLink.objects.create(username=user1, url=TEST_URLS[2])
        VisitedLink.objects.create(username=user1, url=TEST_URLS[2],
                                   is_seattle=True)

        popular_links = VisitedLink.get_popular()

        self.assertEquals(len(popular_links), 3)
        self.assertEquals(popular_links[0]['url'], TEST_URLS[0])
        self.assertEquals(popular_links[0]['popularity'], 4)
        self.assertEquals(popular_links[1]['url'], TEST_URLS[2])
        self.assertEquals(popular_links[1]['popularity'], 2)
        self.assertEquals(popular_links[2]['url'], TEST_URLS[1])
        self.assertEquals(popular_links[2]['popularity'], 1)

        popular_links = VisitedLink.get_popular(is_student=True)
        self.assertEquals(len(popular_links), 1)
        self.assertEquals(popular_links[0]['url'], TEST_URLS[0])
        self.assertEquals(popular_links[0]['popularity'], 1)

        popular_links = VisitedLink.get_popular(is_seattle=True)
        self.assertEquals(len(popular_links), 2)
        self.assertEquals(popular_links[0]['url'], TEST_URLS[0])
        self.assertEquals(popular_links[0]['popularity'], 4)
        self.assertEquals(popular_links[1]['url'], TEST_URLS[2])
        self.assertEquals(popular_links[1]['popularity'], 1)

    def test_popular_multi_labels(self):
        VisitedLink.objects.all().delete()

        user1 = 'basic1'
        user2 = 'basic2'
        user3 = 'basic3'

        VisitedLink.objects.create(username=user1, url=TEST_URLS[0], label="x",
                                   is_student=True, is_seattle=True)
        VisitedLink.objects.create(username=user2, url=TEST_URLS[0], label="x",
                                   is_seattle=True)

        VisitedLink.objects.create(username=user1, url=TEST_URLS[1], label="x",
                                   is_student=True, is_seattle=True)
        VisitedLink.objects.create(username=user2, url=TEST_URLS[1], label="x",
                                   is_seattle=True)
        VisitedLink.objects.create(username=user3, url=TEST_URLS[1], label="y",
                                   is_seattle=True)

        popular_links = VisitedLink.get_popular()
        self.assertEquals(len(popular_links), 2)
        self.assertEquals(popular_links[0]['url'], TEST_URLS[1])
        self.assertEquals(popular_links[0]['popularity'], 9)
        self.assertEquals(popular_links[0]['labels'], ['x', 'y'])

        self.assertEquals(popular_links[1]['url'], TEST_URLS[0])
        self.assertEquals(popular_links[1]['popularity'], 4)
        self.assertEquals(popular_links[1]['labels'], ['x'])
