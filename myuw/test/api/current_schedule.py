from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from unittest2 import skipIf
from myuw.test.api import missing_url, get_user, get_user_pass
from django.test.utils import override_settings
import json


FDAO_SWS = 'restclients.dao_implementation.sws.File'
Session = 'django.contrib.sessions.middleware.SessionMiddleware'
Common = 'django.middleware.common.CommonMiddleware'
CsrfView = 'django.middleware.csrf.CsrfViewMiddleware'
Auth = 'django.contrib.auth.middleware.AuthenticationMiddleware'
RemoteUser = 'django.contrib.auth.middleware.RemoteUserMiddleware'
Message = 'django.contrib.messages.middleware.MessageMiddleware'
XFrame = 'django.middleware.clickjacking.XFrameOptionsMiddleware'
UserService = 'userservice.user.UserServiceMiddleware'
AUTH_BACKEND = 'django.contrib.auth.backends.ModelBackend'


@skipIf(missing_url("myuw_current_schedule"), "myuw urls not configured")
@override_settings(RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS,
                   MIDDLEWARE_CLASSES=(Session,
                                       Common,
                                       CsrfView,
                                       Auth,
                                       RemoteUser,
                                       Message,
                                       XFrame,
                                       UserService,
                                       ),
                   AUTHENTICATION_BACKENDS=(AUTH_BACKEND,)
                   )
class TestSchedule(TestCase):
    def setUp(self):
        self.client = Client()

    def test_javerage_current_term(self):

        response = self.get_current_schedule_res('javerage')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)

        self.assertEquals(data["term"]["year"], 2013)
        self.assertEquals(data["term"]["quarter"], 'Spring')
        self.assertEquals(len(data["sections"]), 5)

        phys = self.get_section(data, 'PHYS', '121', 'A')

        self.assertEquals(phys['canvas_url'],
                          'https://canvas.uw.edu/courses/249652')
        self.assertEquals(phys['canvas_name'], 'MECHANICS')
        self.assertEquals(
            phys['lib_subj_guide'],
            'http://guides.lib.uw.edu/friendly.php' +
            '?s=research/physics_astronomy'
        )

        train = self.get_section(data, 'TRAIN', '101', 'A')
        self.assertNotIn('canvas_url', train)

    def test_none_current_term(self):

        response = self.get_current_schedule_res('none')
        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.content, 'Data not found')

    def test_eight_current_term(self):

        response = self.get_current_schedule_res('eight')
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(data["term"]["year"], 2013)
        self.assertEquals(data["term"]["quarter"], 'Spring')
        self.assertEquals(len(data["sections"]), 8)

        arctic = self.get_section(data, 'ARCTIC', '200', 'A')
        self.assertEquals(arctic['lib_subj_guide'],
                          'http://guides.lib.uw.edu/tacoma/art')

    def test_jbothell_current_term(self):

        response = self.get_current_schedule_res('jbothell')
        self.assertEquals(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEquals(data["term"]["year"], 2013)
        self.assertEquals(data["term"]["quarter"], 'Spring')

        bcwrit = self.get_section(data, 'BCWRIT', '500', 'A')
        self.assertEquals(bcwrit['lib_subj_guide'],
                          'http://guides.lib.uw.edu/bothell/')
        bisseb = self.get_section(data, 'BISSEB', '259', 'A')
        self.assertEquals(
            bisseb['lib_subj_guide'],
            'http://guides.lib.uw.edu/bothell/businternational')

    def test_missing_current_term(self):

        response = self.get_current_schedule_res('jerror')
        self.assertEquals(response.status_code, 543)

    def test_summer_terms(self):

        response = self.get_current_schedule_res('javerage', '2013-07-06')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)

        self.assertEquals(data["term"]["year"], 2013)
        self.assertEquals(data["term"]["quarter"], 'Summer')
        self.assertEquals(data["summer_term"], "a-term")

        response = self.get_current_schedule_res('javerage', '2013-07-25')
        data = json.loads(response.content)
        self.assertEquals(data["summer_term"], "b-term")

    def get_current_schedule_res(self, user, date=None):

        url = reverse('myuw_current_schedule')
        get_user(user)
        self.client.login(username=user,
                          password=get_user_pass(user))
        if date is not None:
            session = self.client.session
            session["myuw_override_date"] = date
            session.save()

        return self.client.get(url)

    def get_section(self, data, abbr, number, section_id):
        for section in data['sections']:
            if section['curriculum_abbr'] == abbr and\
                    section['course_number'] == number and\
                    section['section_id'] == section_id:

                return section

        self.fail('Did not find course %s %s %s' % (abbr, number, section_id))
