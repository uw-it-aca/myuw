from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

def missing_url(name):
    try:
        url = reverse(name)
    except Exception as ex:
        return True

    return False

def get_user(username):
    try:
        user = User.objects.get(username=username)
        return user
    except Exception as ex:
        user = User.objects.create_user(username, password='pass')
        return user

def get_user_pass(username):
    return 'pass'
