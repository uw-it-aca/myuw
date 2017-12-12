from django.conf import settings


def get_calendar_time_zone():
    return getattr(settings, 'TRUMBA_CALENDAR_TIMEZONE',
                   'America/Los_Angeles')


def get_mailman_courserequest_recipient():
    return getattr(settings, 'MAILMAN_COURSEREQUEST_RECIPIENT', None)


def get_google_search_key():
    return getattr(settings, "GOOGLE_SEARCH_KEY", None)


def get_legacy_url():
    return getattr(settings, "MYUW_USER_SERVLET_URL",
                   "https://myuw.washington.edu/servlet/user")


def get_logout_url():
    return getattr(settings, "LOGOUT_URL", "/Shibboleth.sso/Logout")
