# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from myuw.models import UserCourseDisplay
from myuw.dao.instructor_schedule import check_section_instructor,\
    get_section_by_label
from myuw.dao.pws import get_person_of_current_user
from myuw.dao.user import get_user_model


def set_pin_on_teaching_page(request,
                             section_label,
                             pin=True):
    """
    if pin=True, pin the section on teaching page
    if pin=False, unpin the section from teaching page
    @except InvalidSectionID
    @except NotSectionInstructorException
    @except UserCourseDisplay.DoesNotExist
    """
    section = get_section_by_label(section_label)
    check_section_instructor(section, get_person_of_current_user(request))

    # not to pin a primary section
    if section.is_primary_section:
        return False

    UserCourseDisplay.set_pin(get_user_model(request),
                              section_label, pin)
    return True
