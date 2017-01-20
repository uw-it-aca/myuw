import os
from unittest2 import skipIf
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from django.test import TestCase
from myuw.test import get_user, get_user_pass
from django.urls import NoReverseMatch


def missing_url(name, kwargs=None):
    try:
        reverse(name, kwargs=kwargs)
    except NoReverseMatch as ex:
        print "NoReverseMatch: %s" % ex
        return True

    return False


def require_url(url, message='myuw urls not configured', kwargs=None):
    if "FORCE_VIEW_TESTS" in os.environ:
        return skipIf(False, message)
    return skipIf(missing_url(url, kwargs), message)


Session = 'django.contrib.sessions.middleware.SessionMiddleware'
Common = 'django.middleware.common.CommonMiddleware'
CsrfView = 'django.middleware.csrf.CsrfViewMiddleware'
Auth = 'django.contrib.auth.middleware.AuthenticationMiddleware'
RemoteUser = 'django.contrib.auth.middleware.RemoteUserMiddleware'
Message = 'django.contrib.messages.middleware.MessageMiddleware'
XFrame = 'django.middleware.clickjacking.XFrameOptionsMiddleware'
UserService = 'userservice.user.UserServiceMiddleware'
AUTH_BACKEND = 'django.contrib.auth.backends.ModelBackend'
standard_test_override = override_settings(
    MIDDLEWARE_CLASSES=(Session,
                        Common,
                        CsrfView,
                        Auth,
                        RemoteUser,
                        Message,
                        XFrame,
                        UserService,),
    AUTHENTICATION_BACKENDS=(AUTH_BACKEND,))


@standard_test_override
class MyuwApiTest(TestCase):

    def set_user(self, user):
        get_user(user)
        self.client.login(username=user,
                          password=get_user_pass(user))

    def set_date(self, date):
        session = self.client.session
        session['myuw_override_date'] = date
        session.save()

    def get_response_by_reverse(self, url_reverse, *args, **kwargs):
        url = reverse(url_reverse, *args, **kwargs)
        return self.client.get(url)
