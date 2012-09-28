from django.conf import settings
from myuw_mobile.models import User

class UserService:
    _session = None

    def __init__(self, session):
        self._session = session

    def get_user(self):
        override = self.get_override_user()
        if override is not None and len(override) > 0:
            return override

        actual = self.get_original_user()
        if actual is None or len(actual) == 0:
            self._get_logged_in_user()
            actual = self.get_original_user()

        return actual

    def get_original_user(self):
        if "_us_user" in self._session:
            return self._session["_us_user"]

    def get_override_user(self):
        if "_us_override" in self._session:
            return self._session["_us_override"]

    def set_user(self, user):
        self._session["_us_user"] = user

    def set_override_user(self, override):
        self._session["_us_override"] = override

    def clear_override(self):
        self._session["_us_override"] = None

    def _get_logged_in_user(self):
        if settings.DEBUG:
            netid = 'eight'
        else:
            netid = request.user.username

        if netid is None:
            raise("Must have a logged in user when DEBUG is off")

        self.clear_override()
        self.set_user(netid)

    # the get_user / get_original_user / get_override_user should all really
    # be returning user models.  But, i don't want to be serializing that
    # data for each request.  So for now:
    def get_user_for_netid(self, netid):
        in_db = User.objects.filter(uwnetid=netid)

        if len(in_db) > 0:
            return in_db[0]

        new = User()
        new.uwnetid = netid
        new.save()

        return new
