# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This module encapsulates the interactions with the uw_person_data_store
"""

import json
import logging
import traceback
from uw_person_client.clients.core_client import UWPersonClient
from myuw.util.cache import MyUWMemcachedCache
from myuw.logger.timer import Timer
from myuw.logresp import log_msg, log_exception


logger = logging.getLogger(__name__)
cache_client = MyUWMemcachedCache()
PDS_SERVICE_NAME = 'person_data_store'
PDS_TYPE_STUD = "application_type_credits"
PDS_TYPE_QUAR = "quarter_completed"


def get_cache_key(data_type, sys_key):
    return ("{}_{}".format(data_type, sys_key))


def clear_cached_data(key):
    cache_client.deleteCache(PDS_SERVICE_NAME, key)


def get_cached_data(key):
    return cache_client.getCache(PDS_SERVICE_NAME, key)


def set_cache_data(key, value, force_update=True):
    if force_update:
        clear_cached_data(key)
    cache_client.updateCache(PDS_SERVICE_NAME, key, value)


class PdsClient(UWPersonClient):

    def get_application_type_credits(self):
        try:
            timer = Timer()
            sqla_student = self.DB.session.query(self.DB.Student).filter(
                self.DB.Student.enroll_status_code == '12'
            )  # last enrolled (have registered)

            for item in sqla_student.all():
                set_cache_data(
                    get_cache_key(PDS_TYPE_STUD, sqla_student.system_key),
                    json.dumps(
                        {
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
                    ))
            log_msg(logger, timer, PDS_TYPE_STUD)
        except Exception as err:
            logger.error(err)
            log_exception(logger, PDS_TYPE_STUD, traceback)

    def get_quarters_completed(self):
        try:
            timer = Timer()
            sqla_student = self.DB.session.query(
                self.DB.Transcript).join(self.DB.Student).join(
                    self.DB.Term, self.DB.Transcript.tran_term).filter(
                    self.DB.Transcript.enoll_status == '12'
                )  # enrolled in the term

            for item in sqla_student.all():
                set_cache_data(
                    get_cache_key(PDS_TYPE_QUAR, sqla_student.system_key),
                    json.dumps(
                        {
                            "year": sqla_student.year,
                            "quarter": sqla_student.quarter
                        }
                    ))
            log_msg(logger, timer, PDS_TYPE_QUAR)
        except Exception as err:
            logger.error(err)
            log_exception(logger, PDS_TYPE_QUAR, traceback)


def load_cache():
    pds_client = PdsClient()
    pds_client.get_application_type_credits()
    pds_client.get_quarters_completed()
