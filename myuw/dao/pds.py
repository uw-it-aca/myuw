# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This module encapsulates the interactions with the uw_person_data_store
"""

import logging
from sqlalchemy import or_, and_
from uw_person_client import UWPersonClient
from sis_provisioner.exceptions import EmptyQueryException


logger = logging.getLogger(__name__)


class PdsClient(UWPersonClient):
    students = {}
    quarters_completed = {}

    def get_students(self):
        try:
            sqla_student = self.DB.session.query(self.DB.Student).filter(
                self.DB.Student.enroll_status_code == '12'
            )  # registered student

            for item in sqla_student.all():
                self.students[sqla_student.system_key] = {
                    "application_status_code":
                        sqla_student.application_type_code,
                    "total_deductible_credits":
                        sqla_student.total_deductible_credits,
                    "total_extension_credits":
                        sqla_student.total_extension_credits,
                    "total_grade_attempted":
                        sqla_student.total_grade_attempted,
                    "total_lower_div_transfer_credits":
                        sqla_student.total_lower_div_transfer_credits,
                    "total_upper_div_transfer_credits ":
                        sqla_student.total_upper_div_transfer_credits,
                    "total_non_graded_credits":
                        sqla_student.total_non_graded_credits
                }
        except Exception as err:
            logger.error(err)

    def get_quarters_completed(self):
        try:
            sqla_student = self.DB.session.query(
                self.DB.Transcript).join(self.DB.Student).join(
                    self.DB.Term, Transcript.tran_term).filter(
                    self.DB.Transcript.enoll_status == '12'
                )  # enrolled

            for item in sqla_student.all():
                self.quarters_completed[sqla_student.system_key] = {
                    "year":
                        sqla_student.year,
                    "quarter":
                        sqla_student.quarter
                }
        except Exception as err:
            logger.error(err)
