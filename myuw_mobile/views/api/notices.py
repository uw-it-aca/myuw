import logging
import json
from django.http import HttpResponse
from myuw_mobile.views.rest_dispatch import RESTDispatch
from myuw_mobile.dao.notice import get_notices_for_current_user
from myuw_mobile.logger.timer import Timer
from myuw_mobile.logger.logresp import log_success_response
from datetime import datetime


class Notices(RESTDispatch):
    """
    Performs actions on resource at /api/v1/notices/.
    """

    def GET(self, request):
        """
        GET returns 200 with a list of notices for the current user
        """
        timer = Timer()
        logger = logging.getLogger(__name__)
        notices = get_notices_for_current_user()
        notice_json = self._get_json(notices)
        logger.debug(notice_json)
        log_success_response(logger, timer)
        return HttpResponse(json.dumps(notice_json))



    def _get_json(self, notices):

        notice_json = {
            "holds": [],
            "today": [],
            "week": [],
            'future': []
        }
        today = datetime.now()

        for notice in notices:
            data = notice.json_data()
            data['id_hash'] = notice.id_hash
            data['is_read'] = notice.is_read
            data['category'] = notice.custom_category

            if notice.custom_category == "Holds":
                notice_json['holds'].append(data)
            else:
                for attr in notice.attributes:
                    if attr.data_type == "date":
                        date = datetime.strptime(attr.get_value(), "%Y-%m-%d")
                        if date.strftime("%j") == today.strftime("%j"):
                            notice_json["today"].append(data)
                        if date.strftime("%V") == today.strftime("%V"):
                            notice_json["week"].append(data)
                        if date > today:
                            notice_json["future"].append(data)
        return notice_json

