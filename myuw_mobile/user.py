from django.http import HttpRequest
from django.conf import settings
from myuw_mobile.models import User
import logging

class UserService:
    _session = None
    _logger = logging.getLogger('myuw_mobile.user.UserService')

    def __init__(self, request):
        self._session = request.session
        self._get_real_ip(request)
        self._log_data = {'clientip':request.META['REMOTE_ADDR'],
                          'user': None,
                          'useragent': request.META['HTTP_USER_AGENT'],
                          'path': request.get_full_path() }

    def _get_real_ip(self, request):
        try:
            real_ip = request.META['HTTP_X_FORWARDED_FOR']
        except KeyError:
            pass
        else:
            # HTTP_X_FORWARDED_FOR can be a comma-separated list of IPs.
            # Take just the first one.
            real_ip = real_ip.split(",")[0]
            request.META['REMOTE_ADDR'] = real_ip

    def get_log_user_info(self):
        """
        Return a dictionary of user, accessed path, and client information for logging
        """
        self._log_data['user'] = self._get_userid_for_log() 
        return self._log_data
    
    def _get_userid_for_log(self):
        """
        Return <actual user netid> acting_as: <override user netid> if
        the user is acting as someone else, otherwise <actual user netid>
        """
        override_userid = self.get_override_user()
        actual_userid = self.get_original_user()
        if override_userid:
            log_userid = actual_userid + ' acting_as: ' + override_userid
        else:
            log_userid = actual_userid
        return log_userid

    def get_user(self):
        override = self.get_override_user()
        if override and len(override) > 0:
            return override

        actual = self.get_original_user()
        if not actual or len(actual) == 0:
            return self._get_authenticated_user()
        return actual

    def _get_authenticated_user(self):
        if settings.DEBUG:
            netid = 'javerage'
        else:
            netid = request.user.username

        if netid:
            self.clear_override()
            self.set_user(netid)
        else:
            self._logger.error("_get_authenticated_user no valid netid!",
                               self.get_logging_user_info())
        return netid

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
