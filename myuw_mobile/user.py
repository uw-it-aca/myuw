from django.http import HttpRequest
from django.conf import settings
import logging
from myuw_mobile.models import User


class UserService:
    _user_data = {}
    logger = logging.getLogger('myuw_mobile.user.UserService')

    
    def _require_middleware(self):
        if not "initialized" in UserService._user_data:
            print "You need to have this line in your MIDDLEWARE_CLASSES:"
            print "'myuw_mobile.user.UserServiceMiddleware',"

            raise Exception("You need the UserServiceMiddleware")

    def get_user(self):
        self._require_middleware()

        override = self.get_override_user()
        if override and len(override) > 0:
            return override

        actual = self.get_original_user()
        if not actual or len(actual) == 0:
            return self._get_authenticated_user()
        return actual

    def get_original_user(self):
        if "original_user" in UserService._user_data:
            return UserService._user_data["original_user"]

    def get_override_user(self):
        if "override_user" in UserService._user_data:
            return UserService._user_data["override_user"]

    def set_user(self, user):
        UserService._user_data["original_user"] = user
        UserService._user_data["session"]["_us_user"] = user

    def set_override_user(self, override):
        UserService._user_data["override_user"] = override
        UserService._user_data["session"]["_us_override"] = override

    def clear_override(self):
        UserService._user_data["override_user"] = None
        UserService._user_data["session"]["_us_override"] = None

    # the get_user / get_original_user / get_override_user 
    # should all really be returning user models.  But, i don't want 
    # to be serializing that data for each request. So for now:
    def get_user_model(self):
        netid = self.get_user()
        in_db = User.objects.filter(uwnetid=netid)

        if len(in_db) > 0:
            return in_db[0]

        new = User()
        new.uwnetid = netid
        new.save()

        return new

class UserServiceMiddleware(object):

    logger = logging.getLogger('myuw_mobile.user.UserServiceMiddleware')

    def process_request(self, request):
        UserService._user_data["initialized"] = True

        session = request.session
        UserService._user_data["session"] = session

        if not "_us_user" in session:
            user = self._get_authenticated_user(request)
            if user:
                UserService._user_data["original_user"] = user
                UserService._user_data["session"]["_us_user"] = user
        else:
            UserService._user_data["original_user"] = session["_us_user"]

        if "_us_override" in session:
            UserService._user_data["override_user"] = session["_us_override"]

    def process_response(self, request, response):
        UserService._user_data = {}
        return response

    def _get_authenticated_user(self, request):
        netid = None
        if settings.DEBUG:
            netid = 'javerage'
        else:
            netid = request.user.username

        return netid


