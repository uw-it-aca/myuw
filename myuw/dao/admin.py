import logging
from myuw.util.settings import get_myuw_astra_group_stem,\
    get_myuw_admin_group, get_myuw_override_group
from myuw.dao import get_netid_of_original_user
from myuw.dao.gws import gws


logger = logging.getLogger(__name__)
MYUW_ADMIN_GROUP = get_myuw_admin_group()
MYUW_OVERRIDE_GROUP = get_myuw_override_group()
MYUW_ASTRA_GROUP_STEM = get_myuw_astra_group_stem()


def _search_groups(uwnetid):
    group_refs = gws.search_groups(member=uwnetid,
                                   stem=MYUW_ASTRA_GROUP_STEM,
                                   scope="all",
                                   type="effective")
    is_admin = False
    override = False
    if group_refs:
        for gr in group_refs:

            if gr.name == MYUW_ADMIN_GROUP:
                is_admin = True
                break

            if gr.name == MYUW_OVERRIDE_GROUP:
                override = True

    return is_admin, override


def get_myuw_support_role():
    return _search_groups(get_netid_of_original_user())


def is_admin():
    try:
        is_admin, override = get_myuw_support_role()
        return is_admin
    except Exception as ex:
        logger.error("is_admin ==> %s", ex)
        return False


def can_override():
    try:
        is_admin, override = get_myuw_support_role()
        return override or is_admin
    except Exception as ex:
        logger.error("can_override ==> %s", ex)
        return False
