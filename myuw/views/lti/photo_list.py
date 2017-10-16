from django.utils.decorators import method_decorator
from blti.views import BLTILaunchView
from myuw.dao.canvas import sws_course_label, get_viewable_course_sections
from myuw.util.performance import log_response_time
from restclients_core.exceptions import DataFailureException
import re


@method_decorator(log_response_time, name='dispatch')
class LTIPhotoList(BLTILaunchView):
    template_name = 'lti/photo_list.html'
    authorized_role = 'admin'

    def get_context_data(self, **kwargs):
        request = kwargs.get('request')
        blti_data = kwargs.get('blti_params')
        course_id = blti_data.get('custom_canvas_course_id')
        sis_course_id = blti_data.get('lis_course_offering_sourcedid')
        user_id = blti_data.get('custom_canvas_user_id')
        sections = []

        (sws_course_id, sws_instructor_regid) = sws_course_label(sis_course_id)

        try:
            sections = get_viewable_course_sections(course_id, user_id)
            sections.sort(key=lambda section: section.name)
        except DataFailureException as err:
            pass

        return {
            'lti_session_id': request.session.session_key,
            'lti_course_name': blti_data.get('context_label'),
            'sections': sections,
            'section': sws_course_id,
        }
