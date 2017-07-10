from django.test.utils import override_settings
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from userservice.user import UserServiceMiddleware
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
from myuw.dao.class_website import CLASS_WEBSITE_DAO


fdao_class_website_override = use_mock(CLASS_WEBSITE_DAO())


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
