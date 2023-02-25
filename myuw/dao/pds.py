# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This module encapsulates the interactions with the uw_person_data_store
"""

import json
import logging
import traceback
from memcached_clients import MemcacheError
from uw_person_client.clients.core_client import UWPersonClient
from myuw.util.cache import MyUWMemcachedCache, ONE_DAY
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_msg, log_exception


logger = logging.getLogger(__name__)
cache_client = MyUWMemcachedCache()
PDS_TYPE_STUD = "application_type_credits"
PDS_TYPE_QUAR = "quarter_completed"


def get_cache_key(data_type, sys_key):
    return ("person_data_store-{}/{}".format(data_type, sys_key))


def clear_cached_data(key):
    try:
        cache_client.delete(key)
    except (MemcacheError, ConnectionError) as ex:
        logger.error("memcached delete: {}, key: {}".format(ex, key))


def get_cached_data(key):
    return cache_client.get(key)


def set_cache_data(key, value, force_update=True):
    if force_update:
        clear_cached_data(key)
    try:
        cache_client.client.set(key, value, expire=ONE_DAY)
    except (MemcacheError, ConnectionError) as ex:
        logger.error("memcached set: {}, key: {}".format(ex, key))


def cache_application_type_credits(students):
    try:
        timer = Timer()
        for student in students:
            set_cache_data(
                get_cache_key(PDS_TYPE_STUD, student.system_key),
                json.dumps(
                    {
                        "application_status_code":
                            student.application_type_code,
                        "total_deductible_credits":
                            student.total_deductible_credits,
                        "total_extension_credits":
                            student.total_extension_credits,
                        "total_grade_attempted":
                            student.total_grade_attempted,
                        "total_lower_div_transfer_credits":
                            student.total_lower_div_transfer_credits,
                        "total_upper_div_transfer_credits ":
                            student.total_upper_div_transfer_credits,
                        "total_non_graded_credits":
                            student.total_non_graded_credits
                    }
                ))
        log_msg(logger, timer, PDS_TYPE_STUD)
    except Exception as err:
        logger.error(err)
        log_exception(logger, PDS_TYPE_STUD, traceback)


def cache_quarters_completed(students):
    try:
        timer = Timer()
        for student in students:
            quarters_completed = []
            for transcript in student.transcript:
                quarters_completed.append(
                    json.dumps({
                        "year": transcript.tran_term.year,
                        "quarter": transcript.tran_term.quarter
                    }))
            set_cache_data(
                get_cache_key(PDS_TYPE_QUAR, student.system_key),
                json.dumps(quarters_completed))

        log_msg(logger, timer, PDS_TYPE_QUAR)
    except Exception as err:
        logger.error(err)
        log_exception(logger, PDS_TYPE_QUAR, traceback)


def load_cache():
    students = UWPersonClient().get_registered_students(
        include_employee=False,
        include_student=True,
        include_student_transcripts=True,
        include_student_transfers=False,
        include_student_sports=False,
        include_student_advisers=False,
        include_student_majors=False,
        include_student_pending_majors=False
    )
    cache_application_type_credits(students)
    cache_quarters_completed(students)
