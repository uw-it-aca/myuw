import re


def validate(username):
    return _validate(username, r'^[a-z][a-z0-9]{0,7}$')


def validate_shib(username):
    return _validate(username, r'^[a-z][a-z0-9]{0,7}@washington.edu$')


def _validate(username, regex):
    if len(username) == 0:
        return "No override user supplied"

    if username != username.lower():
        return "Usernames must be all lowercase"

    re_personal_netid = re.compile(regex)
    if not re_personal_netid.match(username):
        return ("Username not a valid netid (starts with a letter, "
                "then 0-7 letters or numbers)")

    return None


def transform(username):
    start = username.lower().strip()
    if re.match(".*@.*", start):
        return start

    return "%s@washington.edu" % start
