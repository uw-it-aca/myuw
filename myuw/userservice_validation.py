import re


INVALID_STRING = ("Username not a valid netid (starts with a letter, "
                  "then 0-15 letters, _ or numbers)")
UPPERCASE = "Usernames must be all lowercase"
NO_USER = "No override user supplied"


def validate(username):
    if len(username) == 0:
        return NO_USER

    if username != username.lower():
        return UPPERCASE

    re_personal_netid = re.compile(r'^[a-z][_a-z0-9]{0,15}$', re.I)
    if not re_personal_netid.match(username):
        return INVALID_STRING

    return None
