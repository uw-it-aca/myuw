from uw_sws.person import get_person_by_regid
from myuw.dao.pws import get_regid_of_current_user
from uw_sdbmyuw import get_app_status


def get_applications():
    sws_person = get_person_by_regid(get_regid_of_current_user())

    system_key = sws_person.student_system_key

    applications = get_app_status(system_key)

    response = []

    for application in applications:
        response.append(application.json_data())

    return response
