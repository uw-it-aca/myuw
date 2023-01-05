# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
Define card content as categorized notices so that
they can be marked "new"
"""

from uw_sws.models import Notice


CATEGORIZED_NOTICES = [
    {
        "NoticeCategory": "Degree",
        "NoticeType": "Ceremony",
        "NoticeContent": (
            "<span class=\"notice-title\">Decide if you'd like to " +
            "participate in the UW commencement celebration</span>" +
            "<span class=\"notice-body-with-title\"></span>"
        )
    },
    {
        "NoticeCategory": "Degree",
        "NoticeType": "Diploma",
        "NoticeContent": (
            "<span class=\"notice-title\">How to update your diploma " +
            "name and mailing address</span>" +
            "<span class=\"notice-body-with-title\"></span>"
        )
    },
    {
        "NoticeCategory": "Degree",
        "NoticeType": "SaveWork",
        "NoticeContent": (
            "<span class=\"notice-title\">Save your UW work before " +
            "it is deleted</span>" +
            "<span class=\"notice-body-with-title\"></span>"
        )
    },
    {
        "NoticeCategory": "Degree",
        "NoticeType": "EmailForwarding",
        "NoticeContent": (
            "<span class=\"notice-title\">Keep receiving emails sent " +
            "to your UW address – set up forwarding</span>" +
            "<span class=\"notice-body-with-title\"></span>"
        )
    },
    {
        "NoticeCategory": "Degree",
        "NoticeType": "NextDestination",
        "NoticeContent": (
            "<span class=\"notice-title\">What do graduates do after " +
            "leaving UW?</span>" +
            "<span class=\"notice-body-with-title\"></span>"
        )
    },
    {
        "NoticeCategory": "Teaching",
        "NoticeType": "ClassResAccessible",
        "NoticeContent": (
            "<span class=\"notice-title\">Are your class resources " +
            "accessible for all students?</span>" +
            "<span class=\"notice-body-with-title\"></span>"
        )
    }
]


def get_category_notices(category):
    notices = []
    for notice in CATEGORIZED_NOTICES:
        if notice.get("NoticeCategory") == category:
            notice_obj = Notice()
            notice_obj.notice_category = notice.get("NoticeCategory")
            notice_obj.notice_content = notice.get("NoticeContent")
            notice_obj.notice_type = notice.get("NoticeType")
            notice_obj.attributes = []
            notices.append(notice_obj)
    return notices
