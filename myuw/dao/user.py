import logging
from myuw.models import MigrationPreference
from myuw.dao import get_user_model


logger = logging.getLogger(__name__)


def has_legacy_preference(request):
    try:
        saved = MigrationPreference.objects.get(user=get_user_model(request))
        return saved.use_legacy_site
    except MigrationPreference.DoesNotExist:
        pass
    return False


def display_onboard_message(request):
    try:
        saved = MigrationPreference.objects.get(user=get_user_model(request))
        return saved.display_onboard_message
    except MigrationPreference.DoesNotExist:
        pass
    return False


def is_oldmyuw_user(request):
    if has_legacy_preference(request):
        return True
    return False


def set_no_onboard_message(request):
    return MigrationPreference.set_preference(get_user_model(request),
                                              display_onboard_message=False)


def set_preference_to_new_myuw(request):
    return MigrationPreference.set_preference(get_user_model(request),
                                              use_legacy_site=False)


def set_preference_to_old_myuw(request):
    return MigrationPreference.set_preference(get_user_model(request),
                                              use_legacy_site=True)
