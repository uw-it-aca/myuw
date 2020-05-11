import json
from django.urls import reverse
from myuw.dao.user import get_user_model
from myuw.models import VisitedLinkNew, PopularLink, CustomLink, HiddenLink
from myuw.views.api.link import get_link_data
from myuw.test import get_request_with_user
from myuw.test.api import MyuwApiTest


class TestQuickLinksAPI(MyuwApiTest):

    def test_get_link_data(self):
        data = {'type': 'custom',
                'url': 'www.washington.edu/'
                }
        url, label = get_link_data(data, get_id=False)
        self.assertEquals(url, 'http://www.washington.edu/')
        self.assertEquals(label, 'http://www.washington.edu/')

        data = {'type': 'custom',
                'url': 'www.washington.edu/',
                'label': 'UW Homepage'
                }
        url, label = get_link_data(data, get_id=False)
        self.assertEquals(label, 'UW Homepage')

        data = {'type': 'custom',
                'url': 'www.washington.edu/',
                'label': 'UW Homepage',
                'id': 1
                }
        link_id, url, label = get_link_data(data)
        self.assertEquals(link_id, 1)

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
        req = get_request_with_user('none')
        not_me = get_user_model(req)

        req1 = get_request_with_user('javerage')
        javerage = get_user_model(req1)

        l1 = VisitedLinkNew.objects.create(label="L1",
                                           url="http://example.com",
                                           user=not_me)

        l2 = VisitedLinkNew.objects.create(label="L2",
                                           url="http://uw.edu",
                                           user=javerage)

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
        CustomLink.objects.all().delete()
        self.set_user('javerage')
        url = reverse('myuw_manage_links')

        data = json.dumps({'type': 'custom',
                           'url': 'www.washington.edu/classroom/SMI+401'
                           })

        response = self.client.post(url, data, content_type='application_json')
        self.assertEqual(response.status_code, 200)

        all = CustomLink.objects.all()
        self.assertEqual(len(all), 1)

        self.assertEqual(all[0].url,
                         'http://www.washington.edu/classroom/SMI+401')
        self.assertEqual(all[0].label,
                         'http://www.washington.edu/classroom/SMI+401')

        # Add the same link but w/ protocol
        data = json.dumps({'type': 'custom',
                           'url': 'http://www.washington.edu/classroom/SMI+401'
                           })

        response = self.client.post(url, data, content_type='application_json')
        self.assertEqual(response.status_code, 200)

        all = CustomLink.objects.all()
        self.assertEqual(len(all), 1)

        # https is different
        http_url = 'https://www.washington.edu/classroom/SMI+401'
        data = json.dumps({'type': 'custom',
                           'url': http_url
                           })

        response = self.client.post(url, data, content_type='application_json')
        self.assertEqual(response.status_code, 200)

        all = CustomLink.objects.all()
        self.assertEqual(len(all), 2)
        self.assertEqual(all[0].url,
                         'http://www.washington.edu/classroom/SMI+401')
        self.assertEqual(all[1].url,
                         'https://www.washington.edu/classroom/SMI+401')

        # not http/https url
        data = json.dumps({
                'type': 'custom',
                'url': 'webcal://www.trumba.com/calendars/sea_acad-cal.ics'
                })

        response = self.client.post(url, data, content_type='application_json')
        self.assertEqual(response.status_code, 200)
        all = CustomLink.objects.all()
        self.assertEqual(len(all), 3)

    def test_edit_custom_link(self):
        CustomLink.objects.all().delete()
        self.set_user('javerage')
        url = reverse('myuw_manage_links')
        # add link
        data = json.dumps({'type': 'custom',
                           'url': 'www.washington.edu/classroom/SMI+401'
                           })

        response = self.client.post(url, data, content_type='application_json')
        self.assertEqual(response.status_code, 200)
        all = CustomLink.objects.all()
        self.assertEqual(len(all), 1)
        # edit
        link_id = all[0].pk
        data = json.dumps({'type': 'custom-edit',
                           'url': 'http://example.com',
                           'label': 'Just example',
                           'id': link_id,
                           })
        response = self.client.post(url, data, content_type='application_json')
        self.assertEqual(response.status_code, 200)
        all = CustomLink.objects.all()
        self.assertEquals(len(all), 1)
        link = all[0]
        self.assertEquals(link.url, 'http://example.com')
        self.assertEquals(link.label, 'Just example')

        # Make sure links actually have a label...
        data = json.dumps({'type': 'custom-edit',
                           'url': 'www.washington.edu/classroom/SMI+401',
                           'label': '     ',
                           'id': link_id,
                           })

        response = self.client.post(url, data, content_type='application_json')
        self.assertEqual(response.status_code, 200)

        all = CustomLink.objects.all()
        self.assertEquals(len(all), 1)
        link = all[0]
        self.assertEquals(link.url, 'http://www.washington.edu/'
                                    'classroom/SMI+401')
        self.assertEquals(link.label, 'http://www.washington.edu/'
                                      'classroom/SMI+401')

    def test_remove_link(self):
        CustomLink.objects.all().delete()

        # Add a link as 2 users, make sure we can remove ours, but not theirs
        self.set_user('javerage')
        url = reverse('myuw_manage_links')
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

    def test_remove_default_by_url(self):
        HiddenLink.objects.all().delete()
        self.set_user('javerage')
        url = reverse('myuw_manage_links')

        # add HiddenLink
        data = json.dumps({'type': 'hide',
                           'id': 'http://example.com'})
        response = self.client.post(url, data, content_type='application_json')
        self.assertEquals(response.status_code, 200)
        all = HiddenLink.objects.all()
        self.assertEqual(len(all), 1)
        self.assertEqual(all[0].url, 'http://example.com')
        # same link second time
        response = self.client.post(url, data, content_type='application_json')
        self.assertEquals(response.status_code, 200)
        all = HiddenLink.objects.all()
        self.assertEqual(len(all), 1)
        # Hide a non-default
        data = json.dumps({'type': 'hide',
                           'url': 'http://uw.edu'})
        response = self.client.post(url, data, content_type='application_json')
        self.assertEquals(response.status_code, 404)
        all = HiddenLink.objects.all()
        self.assertEqual(len(all), 1)

    def test_disable_action(self):
        with self.settings(DEBUG=False,
                           MYUW_DISABLE_ACTIONS_WHEN_OVERRIDE=True):
            self.set_user('javerage')
            self.set_userservice_override('bill')
            url = reverse('myuw_manage_links')
            data = json.dumps({'type': 'custom',
                               'url': 'www.washington.edu'})
            response = self.client.post(url, data,
                                        content_type='application_json')
            self.assertEqual(response.status_code, 403)
