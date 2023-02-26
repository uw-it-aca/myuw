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


class PdsClient(UWPersonClient):

    def load_cache(self):
        try:
            timer = Timer()
            sqla_students = self.DB.session.query(
                self.DB.Transcript).join(self.DB.Student).join(
                    self.DB.Term, self.DB.Transcript.tran_term).filter(
                    self.DB.Transcript.enoll_status == '12'
                )  # enrolled in the term

            for student in sqla_students.all():
                quarters_completed = []
                for transcript in student.transcript:
                    quarters_completed.append(
                        json.dumps({
                            "year": transcript.tran_term.year,
                            "quarter": transcript.tran_term.quarter
                        }))
                set_cache_data(
                    student.student_number,
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
                                student.total_non_graded_credits,
                            "quarters_completed": quarters_completed
                        }
                    ))
            log_msg(logger, timer, "load_cache")
        except Exception:
            log_exception(logger, "load_cache", traceback)
