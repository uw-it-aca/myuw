# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
This module encapsulates the interactions with the uw_person_data_store
"""

import json
import logging
import traceback
from memcached_clients import MemcacheError
from sqlalchemy import and_
from uw_person_client.clients.core_client import UWPersonClient
from myuw.util.cache import MyUWMemcachedCache, ONE_DAY
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_msg, log_exception


logger = logging.getLogger(__name__)
cache_client = MyUWMemcachedCache()
DATA_TYPE = "application_type_credits_quarters_completed"


def get_cache_key(student_number):
    return ("person_data_store/{}/{}".format(DATA_TYPE, student_number))


def clear_cached_data(student_number):
    key = get_cache_key(student_number)
    try:
        return cache_client.delete(key)
    except (MemcacheError, ConnectionError) as ex:
        logger.error("memcached delete {}: {}".format(key, ex))


def get_cached_data(student_number):
    key = get_cache_key(student_number)
    logger.info("memcached get {}".format(key))
    return cache_client.get(key)


def set_cache_data(student_number, value, force_update=True):
    if force_update:
        res = clear_cached_data(student_number)
        logger.error("memcached delete {}: {}".format(student_number, res))
    key = get_cache_key(student_number)
    try:
        cache_client.client.set(key, value, expire=ONE_DAY)
        logger.info("memcached set {}, {}".format(key, value))
    except (MemcacheError, ConnectionError) as ex:
        logger.error("memcached set {}, {}: {}".format(key, value, ex))


def cache_application_type_credits(persons):
    try:
        timer = Timer()
        for person in persons:
            set_cache_data(
                get_cache_key(PDS_TYPE_STUD, person.student.system_key),
                json.dumps(
                    {
                        "application_status_code":
                            person.student.application_type_code,
                        "total_deductible_credits":
                            person.student.total_deductible_credits,
                        "total_extension_credits":
                            person.student.total_extension_credits,
                        "total_grade_attempted":
                            person.student.total_grade_attempted,
                        "total_lower_div_transfer_credits":
                            person.student.total_lower_div_transfer_credits,
                        "total_upper_div_transfer_credits ":
                            person.student.total_upper_div_transfer_credits,
                        "total_non_graded_credits":
                            person.student.total_non_graded_credits
                    }
                ))
        log_msg(logger, timer, PDS_TYPE_STUD)
    except Exception as err:
        logger.error(err)
        log_exception(logger, PDS_TYPE_STUD, traceback)


def cache_quarters_completed(persons):
    try:
        timer = Timer()
        for person in persons:
            quarters_completed = []
            for transcript in person.student.transcript:
                quarters_completed.append(
                    json.dumps({
                        "year": transcript.tran_term.year,
                        "quarter": transcript.tran_term.quarter
                    }))
            set_cache_data(
                get_cache_key(PDS_TYPE_QUAR, person.student.system_key),
                json.dumps(quarters_completed))

        log_msg(logger, timer, PDS_TYPE_QUAR)
    except Exception as err:
        logger.error(err)
        log_exception(logger, PDS_TYPE_QUAR, traceback)


def load_cache():
    persons = UWPersonClient().get_registered_students(
        include_employee=False,
        include_student=True,
        include_student_transcripts=True,
        include_student_transfers=False,
        include_student_sports=False,
        include_student_advisers=False,
        include_student_majors=False,
        include_student_pending_majors=False
    )
    cache_application_type_credits(persons)
    cache_quarters_completed(persons)