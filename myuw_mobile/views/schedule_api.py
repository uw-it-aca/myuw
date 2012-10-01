from django.http import HttpResponse
#from django.contrib import auth
#from django.contrib.auth.decorators import login_required
#from django.core.context_processors import csrf
#from django.views.decorators.csrf import csrf_protect
import logging
from django.utils import simplejson as json
from myuw_mobile.dao.sws import Schedule as ScheduleDao
from rest_dispatch import RESTDispatch
from myuw_mobile.user import UserService

class StudClasScheCurQuar(RESTDispatch):
    """
    Performs actions on resource at /api/v1/schedule/current/.
    """
    _logger = logging.getLogger('myuw_mobile.views.schedule_api.StudClasScheCurQuar')

    def GET(self, request):
        """
        GET returns 200 with course section schedule details.
        """

        schedule_dao = ScheduleDao(super(StudClasScheCurQuar,
                                         self).user_service)
        schedule = schedule_dao.get_cur_quarter_schedule()
        colors = schedule_dao.get_colors_for_schedule(schedule)
        buildings = schedule_dao.get_buildings_for_schedule(schedule)

        if (not colors or not buildings or not schedule.json_data()):
            return super(StudClasScheCurQuar, 
                         self).data_not_found(*args, **named_args)

        # Since the schedule is restclients, and doesn't know
        # about color ids, backfill that data
        json_data = schedule.json_data()
        section_index = 0
        for section in schedule.sections:
            section_data = json_data["sections"][section_index]
            color = colors[section.section_label()]
            section_data["color_id"] = color
            section_index += 1

            # Also backfill the meeting building data
            meeting_index = 0
            for meeting in section.meetings:
                mdata = section_data["meetings"][meeting_index]
                if not mdata["building_tbd"]:
                    building = buildings[mdata["building"]]
                    if building is not None:
                        mdata["latitude"] = building.latitude
                        mdata["longitude"] = building.longitude
                        mdata["building_name"] = building.name

                meeting_index += 1

        return HttpResponse(json.dumps(json_data))
