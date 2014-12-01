import re


def validate(username):
    if len(username) == 0:
        return "No override user supplied"

    if username != username.lower():
        return "Usernames must be all lowercase"

    re_personal_netid = re.compile(r'^[a-z][a-z0-9]{0,7}$', re.I)
    if not re_personal_netid.match(username):
        return ("Username not a valid netid (starts with a letter, "
                "then 0-7 letters or numbers)")

    return None
