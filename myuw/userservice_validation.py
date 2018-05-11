import re
from myuw.dao.admin import can_override, is_admin


PERSONAL_NETID = re.compile(r'^[a-z][_A-Za-z0-9]{0,15}$', re.I)
INVALID_STRING = ("Username not a valid netid (starts with a letter, "
                  "then 0-15 letters, _ or numbers)")
NO_USER = "No override user supplied"


def validate(username):
    if len(username) == 0:
        return NO_USER

    if not PERSONAL_NETID.match(username):
        return INVALID_STRING

    return None
