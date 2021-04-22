# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
from myuw.models import MigrationPreference
from myuw.dao.user import get_user_model


logger = logging.getLogger(__name__)


def migration_preference_prefetch():
    def _method(request):
        get_migration_preference(request)
    return [_method]


def get_migration_preference(request):
    if hasattr(request, "migration_preference"):
        return request.migration_preference

    user = get_user_model(request)
    try:
        pref = MigrationPreference.objects.get(user=user)
    except MigrationPreference.DoesNotExist:
        pref = MigrationPreference(user=user,
                                   use_legacy_site=False,
                                   display_onboard_message=True)

    request.migration_preference = pref
    return pref


def _set_migration_preference(request, pref):
    request.migration_preference = pref


def set_no_onboard_message(request):
    pref = MigrationPreference.set_no_onboard_message(get_user_model(request))
    _set_migration_preference(request, pref)
    return pref


def turn_off_pop_up(request):
    pref = MigrationPreference.turn_off_pop_up(get_user_model(request))
    _set_migration_preference(request, pref)
    return pref
