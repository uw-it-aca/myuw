from myuw_mobile.dao.pws import get_netid_of_current_user
from myuw_mobile.models import User


def get_user_model():
    user_netid = get_netid_of_current_user()
    in_db = User.objects.filter(uwnetid=user_netid)
    if len(in_db) > 0:
        return in_db[0]

    new = User()
    new.uwnetid = user_netid
    new.save()
    return new