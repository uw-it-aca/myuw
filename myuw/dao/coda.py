import uw_coda

from myuw.util.thread import Thread


def get_classlist_details(section_label, json_data=None):
    majors = uw_coda.get_majors(section_label, 1)
    print majors

    print section_label
    if json_data is not None:
        print majors
        json_data.update(majors)
        print json_data

    return majors


def get_course_card_details(section_label, json_data=None):
    json_obj = {}
    threads = []

    t = Thread(target=_set_json_fail_rate,
               args=(section_label, json_obj,))
    threads.append(t)
    t.start()

    t = Thread(target=_set_json_cgpa,
               args=(section_label, json_obj,))
    threads.append(t)
    t.start()

    for thread in threads:
        thread.join()

    if json_data is not None:
        json_data.update(json_obj)

    print json_obj

    return json_obj


def _set_json_fail_rate(section_label, json_obj):
    json_obj.update(uw_coda.get_fail_rate(section_label))


def _set_json_cgpa(section_label, json_obj):
    json_obj.update(uw_coda.get_course_cgpa(section_label))
