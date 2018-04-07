import logging
from myuw.models import User
from myuw.dao.pws import get_person_of_current_user


def get_user_model(request):
    if not hasattr(request, "myuw_user_model"):
        person = get_person_of_current_user(request)
        request.myuw_user_model = User.get_user(person.uwnetid,
                                                person.prior_uwnetids)
    return request.myuw_user_model
