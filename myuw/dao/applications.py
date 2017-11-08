from myuw.dao.pws import get_regid_of_current_user, get_person_by_regid
from uw_sdbmyuw import get_app_status


def get_applications():
    sws_person = get_person_by_regid(get_regid_of_current_user())

    system_key = sws_person.student_system_key

    applications = get_app_status(system_key)

    response = []

    for application in applications:
        app = application.json_data()

        if app['is_freshman']:
            app['type'] = "Freshman"
        elif app['is_international_post_bac']:
            app['type'] = "International Post Baccalaureate"
        elif app['is_ug_non_matriculated']:
            app['type'] = "Nonmatriculated"
        elif app['is_transfer']:
            app['type'] = "Transfer"

        response.append(app)

    return response
