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
        user_mig_pref = MigrationPreference.objects.get(user=user)
    except MigrationPreference.DoesNotExist:
        user_mig_pref = MigrationPreference(user=user,
                                            use_legacy_site=False,
                                            display_onboard_message=True)

    request.migration_preference = user_mig_pref
    return user_mig_pref


def set_migration_preference(request, user_mig_pref):
    request.migration_preference = user_mig_pref


def has_legacy_preference(request):
    return get_migration_preference(request).use_legacy_site


def display_onboard_message(request):
    return get_migration_preference(request).display_onboard_message


def is_oldmyuw_user(request):
    if has_legacy_preference(request):
        return True
    return False


def set_no_onboard_message(request):
    obj = MigrationPreference.set_preference(get_user_model(request),
                                             display_onboard_message=False)
    set_migration_preference(request, obj)
    return obj


def set_preference_to_new_myuw(request):
    obj = MigrationPreference.set_preference(get_user_model(request),
                                             use_legacy_site=False)
    set_migration_preference(request, obj)
    return obj


def set_preference_to_old_myuw(request):
    obj = MigrationPreference.set_preference(get_user_model(request),
                                             use_legacy_site=True)
    set_migration_preference(request, obj)
    return obj
