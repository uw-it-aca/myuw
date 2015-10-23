from restclients.dao import SWS_DAO
from myuw.dao.pws import get_netid_of_current_user
from myuw.models import User


def get_user_model():
    user_netid = get_netid_of_current_user()

    user, created = User.objects.get_or_create(uwnetid=user_netid)

    return user


def is_using_file_dao():
    dao = SWS_DAO()._getDAO()
    class_name = dao.__class__.__name__
    return class_name == "File" or class_name == "ByWeek"
