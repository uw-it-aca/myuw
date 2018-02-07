import logging

import uw_coda
from restclients_core.exceptions import DataFailureException

from myuw.util.thread import Thread

logger = logging.getLogger(__name__)


def get_classlist_details(section_label, json_data=None):
    section_label = _process_section_label(section_label)
    try:
        majors = uw_coda.get_majors(section_label, 1)
    except DataFailureException as ex:
        logger.error("%s" % ex)
        return

    if json_data is not None:
        json_data.update(majors)

    return majors


def get_course_card_details(section_label, json_data=None):
    section_label = _process_section_label(section_label)
    json_obj = {}
    threads = []

    t = Thread(target=_set_json_fail_rate,
               args=(section_label, json_obj,))
    threads.append(t)
    t.start()

    for thread in threads:
        thread.join()

    if json_data is not None:
        json_data.update(json_obj)

    return json_obj


def _set_json_fail_rate(section_label, json_obj):
    try:
        json_obj.update(uw_coda.get_fail_rate(section_label))
    except DataFailureException as ex:
        logger.error("%s" % ex)


def _set_json_cgpa(section_label, json_obj):
    try:
        json_obj.update(uw_coda.get_course_cgpa(section_label))
    except DataFailureException as ex:
        logger.error("%s" % ex)


def _process_section_label(section_label):
    section_label = section_label.replace("_", "-")
    indices = section_label.count("-")

    if indices > 4:
        counts = 0
        for i in range(0, len(section_label)):
            if section_label[i] == '-':
                counts += 1

            if counts == 3:
                section_label = section_label[:i] + " " + section_label[i+1:]
                break

    return section_label.replace(" ", "%20")
