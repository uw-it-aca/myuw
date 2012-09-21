from django.http import HttpResponse
#from django.contrib import auth
#from django.contrib.auth.decorators import login_required
#from django.core.context_processors import csrf
#from django.views.decorators.csrf import csrf_protect
import logging
from django.utils import simplejson as json
from myuw_mobile.dao.sws import Schedule as ScheduleDao
from rest_dispatch import RESTDispatch
from pws_util import is_valid_netid
from page import get_netid_from_session

class StudClasScheCurQuar(RESTDispatch):
    """
    Performs actions on resource at /api/v1/schedule/current/.
    """
    _logger = logging.getLogger('myuw_mobile.views.schedule_api.StudClasScheCurQuar')

    def GET(self, request):
        """
        GET returns 200 with course section schedule details.
        """

        netid = get_netid_from_session(request);
        if not netid or not is_valid_netid(netid):
            return super(StudClasScheCurQuar,
                         self).invalid_session(*args, **named_args)

        schedule_dao = ScheduleDao(netid)
        schedule = schedule_dao.get_cur_quarter_schedule()
        colors = schedule_dao.get_colors_for_schedule(schedule)

        if (not colors or 
            not schedule.json_data()):
            return super(StudClasScheCurQuar, 
                         self).data_not_found(*args, **named_args)

        response = HttpResponse(get_colored_sche_json(colors, schedule))
        response.status_code = 200
        return response

def get_colored_sche_json(colors, schedule):
    # Since the schedule is restclients, and doesn't know
    # about color ids, backfill that data
    json_data = schedule.json_data()
    section_index = 0
    for section in schedule.sections:
        section_data = json_data["sections"][section_index]
        color = colors[section.section_label()]
        section_data["color_id"] = color
        section_index += 1
    return json.dumps(json_data) 

