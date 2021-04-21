# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test.utils import override_settings
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from userservice.user import UserServiceMiddleware, UserService
from userservice.user import set_override_user as set_override
from uw_gws.utilities import fdao_gws_override
from uw_pws.util import fdao_pws_override
from uw_sws.util import fdao_sws_override
from uw_libraries.util import fdao_mylib_override, fdao_subject_guide_override
from uw_uwnetid.util import fdao_uwnetid_override
from uw_bookstore.util import fdao_bookstore_override
from uw_iasystem.util import fdao_ias_override
from uw_grad.util import fdao_grad_override
from uw_bookstore.util import fdao_bookstore_override
from uw_canvas.utilities import fdao_canvas_override
from uw_mailman.util import fdao_mailman_override
from uw_upass.util import fdao_upass_override
from uw_hfs.util import fdao_hfs_override
from restclients_core.util.decorators import use_mock


EMAILBACKEND = 'django.core.mail.backends.locmem.EmailBackend'
email_backend_override = override_settings(EMAIL_BACKEND=EMAILBACKEND)
VALIDATION_MODULE = "myuw.authorization.validate_netid"
OVERRIDE_AUTH_MODULE = "myuw.authorization.can_override_user"
ADMIN_AUTH_MODULE = "myuw.authorization.can_proxy_restclient"
auth_override = override_settings(
    USERSERVICE_VALIDATION_MODULE=VALIDATION_MODULE,
    USERSERVICE_OVERRIDE_AUTH_MODULE=OVERRIDE_AUTH_MODULE,
    RESTCLIENTS_ADMIN_AUTH_MODULE=ADMIN_AUTH_MODULE)


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
    UserServiceMiddleware().process_request(now_request)
    return now_request


def set_override_user(username, request=None):
    if request is not None:
        set_override(request, username)
    else:
        UserService().set_override_user(username)


def get_user(username):
    try:
        return User.objects.get(username=username)
    except Exception as ex:
        return User.objects.create_user(
            username, password=get_user_pass(username))


def get_user_pass(username):
    return 'pass'
