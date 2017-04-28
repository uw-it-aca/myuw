from myuw.test.api import MyuwApiTest
from myuw.models import PopularLink, CustomLink, VisitedLink
from django.core.urlresolvers import reverse
import json


class TestQuickLinksAPI(MyuwApiTest):
    def test_add_popular_link(self):
        PopularLink.objects.all().delete()
        CustomLink.objects.all().delete()

        l1 = PopularLink.objects.create(label="Label",
                                        url="http://example.com")

        self.set_user('javerage')

        url = reverse('myuw_manage_links')

        data = json.dumps({'type': 'popular', 'id': l1.pk})
        response = self.client.post(url, data, content_type='application_json')
        self.assertEquals(response.status_code, 200)

        all = CustomLink.objects.all()
        self.assertEquals(len(all), 1)
        self.assertEquals(all[0].url, 'http://example.com')
        self.assertEquals(all[0].label, 'Label')

        data = json.dumps({'type': 'popular', 'id': l1.pk+1})
        response = self.client.post(url, data, content_type='application_json')

        self.assertEquals(response.status_code, 404)

        all = CustomLink.objects.all()
        self.assertEquals(len(all), 1)

        # Test a double post...
        data = json.dumps({'type': 'popular', 'id': l1.pk})
        response = self.client.post(url, data, content_type='application_json')
        self.assertEquals(response.status_code, 200)
        all = CustomLink.objects.all()
        self.assertEquals(len(all), 1)

    def test_add_recent(self):
        VisitedLink.objects.all().delete()
        CustomLink.objects.all().delete()

        l1 = VisitedLink.objects.create(label="L1",
                                        url="http://example.com",
                                        username="not_me")

        l2 = VisitedLink.objects.create(label="L2",
                                        url="http://uw.edu",
                                        username="javerage")

        self.set_user('javerage')

        url = reverse('myuw_manage_links')

        data = json.dumps({'type': 'recent', 'id': l1.pk})
        response = self.client.post(url, data, content_type='application_json')
        self.assertEquals(response.status_code, 404)

        all = CustomLink.objects.all()
        self.assertEquals(len(all), 0)

        data = json.dumps({'type': 'recent', 'id': l2.pk+1})
        response = self.client.post(url, data, content_type='application_json')

        self.assertEquals(response.status_code, 404)
        all = CustomLink.objects.all()
        self.assertEquals(len(all), 0)

        data = json.dumps({'type': 'recent', 'id': l2.pk})
        response = self.client.post(url, data, content_type='application_json')
        self.assertEquals(response.status_code, 200)
        all = CustomLink.objects.all()
        self.assertEquals(len(all), 1)
        self.assertEquals(all[0].url, 'http://uw.edu')
        self.assertEquals(all[0].label, 'L2')

        # Test a double post...
        data = json.dumps({'type': 'recent', 'id': l2.pk})
        response = self.client.post(url, data, content_type='application_json')
        self.assertEquals(response.status_code, 200)
        all = CustomLink.objects.all()
        self.assertEquals(len(all), 1)

    def test_bad_syntax(self):
        self.set_user('javerage')

        url = reverse('myuw_manage_links')

        data = json.dumps({'type': 'xrecent', 'id': 1})
        response = self.client.post(url, data, content_type='application_json')
        self.assertEquals(response.status_code, 404)

        data = json.dumps({'type': 'xrecent'})
        response = self.client.post(url, data, content_type='application_json')
        self.assertEquals(response.status_code, 404)

        data = json.dumps({})
        response = self.client.post(url, data, content_type='application_json')
        self.assertEquals(response.status_code, 404)

        data = "{"
        response = self.client.post(url, data, content_type='application_json')
        self.assertEquals(response.status_code, 404)

    def test_add_pure_custom(self):
        self.set_user('javerage')
        url = reverse('myuw_manage_links')
        CustomLink.objects.all().delete()

        data = json.dumps({'type': 'custom',
                           'url': 'www.washington.edu/classroom/SMI+401'
                           })

        response = self.client.post(url, data, content_type='application_json')
        self.assertEqual(response.status_code, 200)

        all = CustomLink.objects.all()
        self.assertEqual(len(all), 1)

        self.assertEqual(all[0].url,
                         'http://www.washington.edu/classroom/SMI+401')
        self.assertEqual(all[0].label, 'Room Information')

        # Same w/ protocol
        data = json.dumps({'type': 'custom',
                           'url': 'http://www.washington.edu/classroom/SMI+401'
                           })

        response = self.client.post(url, data, content_type='application_json')
        self.assertEqual(response.status_code, 200)

        all = CustomLink.objects.all()
        self.assertEqual(len(all), 1)

        # https is different though
        http_url = 'https://www.washington.edu/classroom/SMI+401'
        data = json.dumps({'type': 'custom',
                           'url': http_url
                           })

        response = self.client.post(url, data, content_type='application_json')
        self.assertEqual(response.status_code, 200)

        all = CustomLink.objects.all()
        self.assertEqual(len(all), 2)

    def test_remove_link(self):
        # Add a link as 2 users, make sure we can remove ours, but not theirs
        self.set_user('javerage')
        url = reverse('myuw_manage_links')
        CustomLink.objects.all().delete()

        data = json.dumps({'type': 'custom',
                           'url': 'www.washington.edu/classroom/SMI+401'
                           })

        response = self.client.post(url, data, content_type='application_json')
        self.assertEqual(response.status_code, 200)

        self.set_user('jpce')
        response = self.client.post(url, data, content_type='application_json')
        self.assertEqual(response.status_code, 200)

        all = CustomLink.objects.all()

        data = json.dumps({'type': 'remove',
                           'id': all[0].pk
                           })

        response = self.client.post(url, data, content_type='application_json')
        self.assertEqual(response.status_code, 404)

        all = CustomLink.objects.all()

        self.assertEqual(len(all), 2)

        data = json.dumps({'type': 'remove',
                           'id': all[1].pk
                           })

        response = self.client.post(url, data, content_type='application_json')
        self.assertEqual(response.status_code, 200)
        all = CustomLink.objects.all()
        self.assertEqual(len(all), 1)
