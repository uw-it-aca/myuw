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


class PdsClient(UWPersonClient):

    def load_cache(self):
        try:
            timer = Timer()
            Transcript = self.DB.Transcript
            Student = self.DB.Student
            Term = self.DB.Term
            student_query = self.DB.session.query(Student).filter(
                Student.enroll_status_code == '12').all()

            for record in student_query:

                term_query = self.DB.session.query(Transcript).join(
                    Term, Transcript.tran_term_id == Term.id).filter(
                        and_(Transcript.student_id == record.id,
                             Transcript.enroll_status == 12)
                        ).all()
                quarters_completed = []
                for term_completed in term_query:
                    quarters_completed.append(
                        json.dumps({
                            "year": term_completed.year,
                            "quarter": term_completed.quarter
                        }))

                set_cache_data(
                    record.student_number,
                    json.dumps(
                        {
                            "application_status_code":
                            record.application_type_code,
                            "total_deductible_credits":
                            record.total_deductible_credits,
                            "total_extension_credits":
                            record.total_extension_credits,
                            "total_grade_attempted":
                            record.total_grade_attempted,
                            "total_lower_div_transfer_credits":
                            record.total_lower_div_transfer_credits,
                            "total_upper_div_transfer_credits ":
                            record.total_upper_div_transfer_credits,
                            "total_non_graded_credits":
                            record.total_non_graded_credits,
                            "quarters_completed": quarters_completed
                        }
                    ))
            log_msg(logger, timer, "load_cache")
        except Exception:
            log_exception(logger, "load_cache", traceback)
