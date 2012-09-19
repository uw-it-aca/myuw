from django.conf import settings

class UserService:
    _session = None

    def __init__(self, session):
        self._session = session

    def get_user(self):
        override = self.get_override_user()
        if override is not None:
            return override

        actual = self.get_original_user()
        if actual is None:
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
            netid = 'javerage'
        else:
            netid = request.user.username

        if netid is None:
            raise("Must have a logged in user when DEBUG is off")

        self.clear_override()
        self.set_user(netid)

