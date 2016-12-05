from django.test.utils import override_settings
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from userservice.user import UserServiceMiddleware

FDAO_SWS = 'restclients.dao_implementation.sws.File'
fdao_sws_override = override_settings(
    RESTCLIENTS_SWS_DAO_CLASS=FDAO_SWS)

FDAO_PWS = 'restclients.dao_implementation.pws.File'
fdao_pws_override = override_settings(
    RESTCLIENTS_PWS_DAO_CLASS=FDAO_PWS
)


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
