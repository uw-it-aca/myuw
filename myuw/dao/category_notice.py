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
            "<span class=\"notice-body-with-title\">" +
            "It is every instructor's <a href=\"http://www.washington.edu/" +
            "admin/rules/policies/SGP/SPCH208.html\">legal and university " +
            "obligation</a> to ensure that class resources are accessible " +
            "for all students. Get started now with the <a href=\"https://" +
            "depts.washington.edu/uwdrs/faculty/course-preparation-" +
            "checklist/\">course preparation checklist</a>.</span>"
        )
    },
    {
        "NoticeCategory": "GradeSubmission",
        "NoticeType": "GradingOpen",
        "NoticeContent": (
            "<span class=\"notice-title\">Review this quarter's " +
            "course settings to avoid issues when submitting grades</span>" +
            "<span class=\"notice-body-with-title\">" +
            "Before grading begins, please review the following:<br>" +
            "<br><ol>" +
            "<li>Will the correct intended grading system be used?</li>" +
            "<ul>" +
            "<li><b>Grading System</b> – Standard or Credit/No Credit</li>" +
            "</ul>" +
            "<li>Can the right people submit grades?</li>"
            "<ul>" +
            "<li><b>Instructors of Record</b> – Only instructors of record " +
            "have access to this course in MyUW and GradePage.</li>" +
            "<li><b>Who Submits Grades</b> – Either primary section " +
            "instructors <b>OR</b> linked section instructors " +
            "(usually TAs) can submit grades through GradePage. " +
            "<li><b>Delegates</b> – In an emergency, delegates can submit " +
            "grades if instructors of record cannot.</li>" +
            "</ul>" +
            "</ol> <br>" +
            "For each course this quarter, <a href=\"/teaching/\">" +
            "verify grade submission information</a>."
            "</span>"
        )
    }
]
# Make sure the line length is less than 80 chars!!


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
