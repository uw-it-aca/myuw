# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from persistent_message.models import Message
from myuw.dao.affiliation import get_all_affiliations
from myuw.dao.gws import is_effective_member
from myuw.dao.term import get_comparison_datetime_with_tz


class BannerMessage(object):

    def __init__(self, request):
        self.request = request
        self.affiliations = get_all_affiliations(request)
        self.now = get_comparison_datetime_with_tz(self.request)

    def get_message_json(self):
        user_msgs = []
        for msg in Message.objects.all().order_by('-begins'):
            if msg.is_active(self.now) and self._matched_with_affi(msg):
                user_msgs.append(msg.to_json(self.now))
        return user_msgs

    def _matched_with_affi(self, msg):
        tags = msg.tags.all()

        if (len(tags) == 0 or  # for everyone
                self._for_alumni(tags) or
                self._for_applicant(tags)):
            return True

        if (self._campus_neutral(tags) and
                (self._employee_affiliation_matched(tags) or
                 self._student_affiliation_matched(tags))):
            return True

        if self._student_affiliation_matched(tags):
            if self._is_stud_campus_matched(tags):
                return True

        if self._employee_affiliation_matched(tags):
            if self._is_employee_campus_matched(tags):
                return True
        return False

    def __match(self, msg_tags, tag_name, tag_group_name):
        for tag in msg_tags:
            if tag.name == tag_name and tag.group.name == tag_group_name:
                return True
        return False

    def _match_campuses(self, msg_tags, tag_name):
        return self.__match(msg_tags, tag_name, 'Campuses')

    def _match_affiliation(self, msg_tags, tag_name):
        return self.__match(msg_tags, tag_name, 'Affiliations')

    def _for_bothell(self, msg_tags):
        return self._match_campuses(msg_tags, 'bothell')

    def _for_seattle(self, msg_tags):
        return self._match_campuses(msg_tags, 'seattle')

    def _for_tacoma(self, msg_tags):
        return self._match_campuses(msg_tags, 'tacoma')

    def _campus_neutral(self, msg_tags):
        return not (
            self._for_bothell(msg_tags) or
            self._for_seattle(msg_tags) or
            self._for_tacoma(msg_tags))

    def _for_alumni(self, msg_tags):
        return (
            self._campus_neutral(msg_tags) and
            self._match_affiliationh(msg_tags, 'alumni') and
            self.affiliations["alumni"])

    def _for_applicant(self, msg_tags):
        return (
            self._campus_neutral(msg_tags) and
            self._match_affiliation(msg_tags, 'applicant') and
            self.affiliations["applicant"])

    def _is_stud_campus_matched(self, msg_tags):
        return (
            self._campus_neutral(msg_tags) or
            self._for_seattle(msg_tags) and self.affiliations['seattle'] or
            self._for_bothell(msg_tags) and self.affiliations['bothell'] or
            self._for_tacoma(msg_tags) and self.affiliations['tacoma'])

    def _is_employee_campus_matched(self, msg_tags):
        return (
            self._campus_neutral(msg_tags) or
            self._for_seattle(msg_tags) and
            self.affiliations['official_seattle'] or
            self._for_bothell(msg_tags) and
            self.affiliations['official_bothell'] or
            self._for_tacoma(msg_tags) and
            self.affiliations['official_tacoma'])

    def _student_affiliation_matched(self, msg_tags):
        return (
            self._match_affiliation(msg_tags, 'grad-student') and
            self.affiliations["grad"] or
            self._match_affiliation(msg_tags, 'gradC2') and
            self.affiliations["grad_c2"] or
            self._match_affiliation(msg_tags, 'intl-student') and
            self.affiliations["intl_stud"] or
            self._match_affiliation(msg_tags, 'undergraduate') and
            self.affiliations["undergrad"] or
            self._match_affiliation(msg_tags, 'undergraduateC2') and
            self.affiliations["undergrad_c2"] or
            self._match_affiliation(msg_tags, 'student-employee') and
            self.affiliations["stud_employee"])

    def _employee_affiliation_matched(self, msg_tags):
        return (
            self._match_affiliation(msg_tags, 'clinician') and
            self.affiliations["clinician"] or
            self._match_affiliation(msg_tags, 'faculty') and
            self.affiliations["faculty"] or
            self._match_affiliation(msg_tags, 'instructor') and
            self.affiliations["instructor"] or
            self._match_affiliation(msg_tags, 'staff-employee') and
            self.affiliations["staff-employee"])
