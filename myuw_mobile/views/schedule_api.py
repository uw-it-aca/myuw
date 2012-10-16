from django.http import HttpResponse
#from django.contrib import auth
#from django.contrib.auth.decorators import login_required
#from django.core.context_processors import csrf
#from django.views.decorators.csrf import csrf_protect
import logging
from django.utils import simplejson as json
from myuw_mobile.dao.sws import Schedule as ScheduleDao
from rest_dispatch import RESTDispatch, data_not_found
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logresp import log_data_not_found_response, log_success_response
from operator import itemgetter

class StudClasScheCurQuar(RESTDispatch):
    """
    Performs actions on resource at /api/v1/schedule/current/.
    """
    def GET(self, request):
        """
        GET returns 200 with course section schedule details.
        """
        
        timer = Timer()
        logger = logging.getLogger('myuw_mobile.views.schedule_api.StudClasScheCurQuar.GET')

        schedule_dao = ScheduleDao()
        schedule = schedule_dao.get_cur_quarter_schedule()
        if not schedule or not schedule.json_data():
            log_data_not_found_response(logger, timer)
            return HttpResponse({})

        colors = schedule_dao.get_colors_for_schedule(schedule)

        buildings = schedule_dao.get_buildings_for_schedule(schedule)

        if not colors:
            if len(schedule.sections) > 0:
                log_data_not_found_response(logger, timer)
                return data_not_found()
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

                for instructor in mdata["instructors"]:
                    if not instructor[
                            "email1"] and not instructor[
                            "email2"] and not instructor[
                            "phone1"] and not instructor[
                            "phone2"] and not instructor[
                            "voicemail"] and not instructor[
                            "fax"] and not instructor[
                            "touchdial"] and not instructor[
                            "address1"] and not instructor[
                            "address2"]:
                        instructor["whitepages_publish"] = False
                meeting_index += 1

        # MUWM-443
        json_data["sections"] = sorted(json_data["sections"],
                                    key=itemgetter('curriculum_abbr',
                                                    'course_number',
                                                    'section_id',
                                    ))

        log_success_response(logger, timer)
        return HttpResponse(json.dumps(json_data))
