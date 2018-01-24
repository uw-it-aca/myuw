from uw_sdbmyuw import get_app_status
from myuw.dao.pws import get_student_system_key_of_current_user


def get_applications(request):
    applications = get_app_status(
        get_student_system_key_of_current_user(request))
    response = []
    for application in applications:
        response.append(application.json_data())
    return response
