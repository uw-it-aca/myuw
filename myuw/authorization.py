import re
from myuw.dao.admin import can_override, is_admin


PERSONAL_NETID = re.compile(r'^[a-z][_A-Za-z0-9]{0,15}$', re.I)
INVALID_STRING = ("Username not a valid netid (starts with a letter, "
                  "then 0-15 letters, _ or numbers)")
NO_USER = "No override user supplied"


def validate_netid(username):
    if len(username) == 0:
        return NO_USER

    if not PERSONAL_NETID.match(username):
        return INVALID_STRING

    return None


def can_override_user(request):
    """
    Return True if the original user has impersonate permission
    """
    if not hasattr(request, "can_override_user"):
        request.can_override_user = can_override()
    return request.can_override_user


def can_proxy_restclient(request, service, url):
    """
    Return True if the original user has admin permission
    """
    if not hasattr(request, "can_proxy_restclient"):
        request.can_proxy_restclient = is_admin()
    return request.can_proxy_restclient


def is_myuw_admin(request):
    return can_proxy_restclient(request, "MyUW Support", "")
