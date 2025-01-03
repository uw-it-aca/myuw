# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
from uw_myplan import Plan
from uw_sws.section import get_section_by_label
from myuw.dao.pws import get_regid_of_current_user


logger = logging.getLogger(__name__)
myplan = Plan()


def get_plan(request, year, quarter):
    plan = myplan.get_plan(
        get_regid_of_current_user(request), year, quarter.lower(), terms=1)

    has_ready_courses = False
    has_unready_courses = False
    ready_count = 0
    unready_count = 0
    has_sections = False
    plan_json = plan.json_data()
    for course in plan_json["terms"][0]["courses"]:
        if course["registrations_available"]:
            has_ready_courses = True
            ready_count = ready_count + 1
            for section in course["sections"]:
                has_sections = True
                curriculum = course["curriculum_abbr"].upper()
                section_id = section["section_id"].upper()
                label = "{},{},{},{}/{}".format(
                    year,
                    quarter.lower(),
                    curriculum,
                    course["course_number"],
                    section_id)

                sws_section = get_section_by_label(label)
                section["section_data"] = sws_section.json_data()
        else:
            if len(course["sections"]):
                has_sections = True
            has_unready_courses = True
            unready_count = unready_count + 1

    plan_json["terms"][0]["has_ready_courses"] = has_ready_courses
    plan_json["terms"][0]["has_unready_courses"] = has_unready_courses
    plan_json["terms"][0]["ready_count"] = ready_count
    plan_json["terms"][0]["unready_count"] = unready_count
    plan_json["terms"][0]["has_sections"] = has_sections
    return plan_json
