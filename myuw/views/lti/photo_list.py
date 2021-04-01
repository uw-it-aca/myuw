# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import re
from django.utils.decorators import method_decorator
from blti.views import BLTILaunchView
from restclients_core.exceptions import DataFailureException
from myuw.dao.canvas import get_viewable_course_sections


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
        section_id = ''

        try:
            sections = get_viewable_course_sections(course_id, user_id)
            section_id = sections[0].sis_section_id
        except (DataFailureException, IndexError) as err:
            pass

        blti_data['authorized_sections'] = [s.sis_section_id for s in sections]
        self.set_session(request, **blti_data)

        return {
            'lti_session_id': request.session.session_key,
            'lti_course_name': blti_data.get('context_label'),
            'sections': sections,
            'section': section_id,
        }
