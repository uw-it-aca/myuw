"""
This module categorize notices based on notice_categorization
"""
import logging
from myuw.dao.notice_categorization import NOTICE_CATEGORIES


logger = logging.getLogger(__name__)
UNKNOWN_CATEGORY_NAME = "Uncategorized"


def categorize_notices(notices):
    for notice in notices:
        map_notice_category(notice)

    notices[:] = [n for n in notices if n.custom_category != "not a notice"]
    # Removing uncategorized notices for MUWM-2343
    notices[:] = [n for n in notices if
                  n.custom_category != UNKNOWN_CATEGORY_NAME]
    return notices


def map_notice_category(notice):
    """
    Set the custom_category, is_critical, location_tags for
    the given notice based on the NOTICE_CATEGORIES defined
    in myuw.dao.notice_categorization
    """
    key = notice.notice_category + "_" + notice.notice_type
    categorization = NOTICE_CATEGORIES.get(key, None)
    if categorization is not None:
        notice.custom_category = categorization["myuw_category"]
        notice.is_critical = categorization["critical"]
        notice.location_tags = categorization["location_tags"]
    else:
        notice.custom_category = UNKNOWN_CATEGORY_NAME
        notice.is_critical = False
        notice.location_tags = None
    return notice
