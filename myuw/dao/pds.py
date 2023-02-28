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


logger = logging.getLogger(__name__)
cache_client = MyUWMemcachedCache()
DATA_TYPE = "application_type_credits_transcript_terms"


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
    logger.debug("memcached get {}".format(key))
    return cache_client.get(key)


def set_cache_data(student_number, value, force_update=True):
    if force_update:
        res = clear_cached_data(student_number)
        logger.debug("memcached delete {}: {}".format(student_number, res))
    key = get_cache_key(student_number)
    try:
        cache_client.client.set(key, value, expire=ONE_DAY)
        logger.debug("memcached set {}: {}".format(key, value))
    except (MemcacheError, ConnectionError) as ex:
        logger.error("memcached set {}, {}: {}".format(key, value, ex))


class PdsClient(UWPersonClient):
    def get_registered_student_data(self):
        return UWPersonClient().get_registered_students(
            include_employee=False,
            include_student=True,
            include_student_transcripts=True,
            include_student_transfers=False,
            include_student_sports=False,
            include_student_advisers=False,
            include_student_majors=False,
            include_student_pending_majors=False
        )

    def load_cache(self):
        try:
            timer = Timer()
            person_records = self.get_registered_student_data()
            for person in person_records:
                # netid = person.uwnetid
                student_record = person.student

                transcript_terms = []
                for trans in student_record.transcripts:
                    transcript_terms.append(
                        {
                            "enroll_status": trans.enroll_status,
                            "year": trans.tran_term.year,
                            "quarter": trans.tran_term.quarter
                        })

                set_cache_data(
                    student_record.student_number,
                    json.dumps(
                        {
                            "application_status_code":
                            student_record.application_type_code,
                            "class_desc":
                            student_record.class_desc,
                            "total_deductible_credits":
                            student_record.total_deductible_credits,
                            "total_extension_credits":
                            student_record.total_extension_credits,
                            "total_grade_attempted":
                            student_record.total_grade_attempted,
                            "total_lower_div_transfer_credits":
                            student_record.total_lower_div_transfer_credits,
                            "total_upper_div_transfer_credits":
                            student_record.total_upper_div_transfer_credits,
                            "total_non_graded_credits":
                            student_record.total_non_graded_credits,
                            "last_enrolled_term": {
                                "year": student_record.academic_term.year,
                                "quarter": student_record.academic_term.quarter
                            },
                            "terms_completed": transcript_terms
                        }
                    ))
            logger.info(
                {
                    'action': "load_cache",
                    'Time': "{} seconds".format(timer.get_elapsed())
                })
        except Exception:
            logger.error(
                {
                    'action': "load_cache",
                    'err': traceback.format_exc(chain=False)
                })
