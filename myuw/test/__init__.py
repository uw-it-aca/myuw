from django.test.utils import override_settings
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from userservice.user import UserServiceMiddleware
from restclients.test import (fdao_uwnetid_override, fdao_pws_override,
                              fdao_sws_override, fdao_libcurr_override,
                              fdao_libacc_override, fdao_ias_override,
                              fdao_hfs_override, fdao_gws_override,
                              fdao_grad_override, fdao_bookstore_override,
                              fdao_canvas_override,  fdao_mailman_override,
                              fdao_upass_override)


EMAILBACKEND = 'django.core.mail.backends.locmem.EmailBackend'
email_backend_override = override_settings(EMAIL_BACKEND=EMAILBACKEND)


def get_request():
    """
    mock request with UserServiceMiddleware initialization
    """
    now_request = RequestFactory().get("/")
    now_request.session = {}
    UserServiceMiddleware().process_request(now_request)
    return now_request


def get_request_with_date(date_str):
    now_request = get_request()
    if date_str:
        now_request.session["myuw_override_date"] = date_str
    return now_request


def get_request_with_user(username, now_request=None):
    if now_request is None:
        now_request = get_request()
    now_request.user = get_user(username)
    return now_request


def get_user(username):
    try:
        user = User.objects.get(username=username)
        return user
    except Exception as ex:
        user = User.objects.create_user(username, password='pass')
        return user


def get_user_pass(username):
    return 'pass'
