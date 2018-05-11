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
    return getattr(settings, "LOGOUT_URL", "/user_logout")


def get_myuwclass_url():
    return getattr(settings, "MYUWCLASS", "myuwclass.asp?cid=")


def get_myuw_admin_group():
    return getattr(settings, "MYUW_ADMIN_GROUP",
                   'u_astratst_myuw_test-support-admin')


def get_myuw_override_group():
    return getattr(settings, "MYUW_OVERRIDE_GROUP",
                   'u_astratst_myuw_test-support-impersonate')


def get_myuw_astra_group_stem():
    return getattr(settings, "MYUW_ASTRA_GROUP_STEM",
                   'u_astratst_myuw')


def get_save_user_actions_when_override():
    return getattr(settings, "MYUW_SAVE_USER_ACTIONS_WHEN_OVERRIDE", True)
