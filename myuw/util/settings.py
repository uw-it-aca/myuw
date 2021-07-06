# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings


def get_calendar_time_zone():
    return getattr(settings, 'TRUMBA_CALENDAR_TIMEZONE',
                   'America/Los_Angeles')


def get_mailman_courserequest_recipient():
    return getattr(settings, 'MAILMAN_COURSEREQUEST_RECIPIENT', None)


def get_google_search_key():
    return getattr(settings, "GOOGLE_SEARCH_KEY", None)


def get_google_analytics_key():
    return getattr(settings, "GOOGLE_ANALYTICS_KEY", None)


def get_django_debug():
    return getattr(settings, "DEBUG", False)


def get_logout_url():
    return getattr(settings, "LOGOUT_URL", "/user_logout")


def no_access_check():
    return getattr(settings, "MYUW_SKIP_ACCESS_CHECK", True)


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


def get_disable_actions_when_override():
    return getattr(settings, "MYUW_DISABLE_ACTIONS_WHEN_OVERRIDE", True)


def get_enabled_features():
    return getattr(settings, "MYUW_ENABLED_FEATURES", [])


def get_myuw_test_access_group():
    return getattr(settings, "MYUW_TEST_ACCESS_GROUP", None)


def get_cronjob_recipient():
    return getattr(settings, 'CRONJOB_RECIPIENT', 'myuw_cron')


def get_cronjob_sender():
    return getattr(settings, 'CRONJOB_SENDER', 'myuw')
