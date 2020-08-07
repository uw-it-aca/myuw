import logging
from myuw.models import User
from myuw.dao import get_netid_of_current_user
from myuw.dao.pws import get_person_of_current_user


def get_updated_user(request):
    """
    Will update the user record
    """
    if not hasattr(request, "myuw_user_model"):
        person = get_person_of_current_user(request)
        request.myuw_user_model = User.get_user(person.uwnetid,
                                                person.prior_uwnetids)
    return request.myuw_user_model


def get_user_model(request):
    """
    Only get user (Will NOT update the record)
    """
    if not hasattr(request, "myuw_user_model"):
        try:
            request.myuw_user_model = User.get_user_by_netid(
                get_netid_of_current_user(request))
        except User.DoesNotExist:
            return get_updated_user(request)
    return request.myuw_user_model


def not_existing_user(request):
    return not User.exists(get_netid_of_current_user(request))
