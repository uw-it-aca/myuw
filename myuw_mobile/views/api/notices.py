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
        return self._get_json_for_date(notices, datetime.now())

    def _get_json_for_date(self, notices, today):
        notice_json = {
            "holds": {"unread_count": 0,
                    "notices": []},

            "today": {"unread_count": 0,
                      "notices": []},
            "week": {"unread_count": 0,
                     "notices": []},
            "next_week": {"unread_count": 0,
                     "notices": []},
            "future": {"unread_count": 0,
                       "notices": []},
            "total_unread": 0
        }

        for notice in notices:
            data = notice.json_data()
            data['id_hash'] = notice.id_hash
            data['is_read'] = notice.is_read
            data['category'] = notice.custom_category
            #total count
            if notice.is_read is False:
                notice_json["total_unread"] += 1

            #split into UX defined categories
            if notice.custom_category == "Holds":
                notice_json["holds"]["notices"].append(data)
                if notice.is_read is False:
                    notice_json["holds"]["unread_count"] += 1
            else:
                for attr in notice.attributes:
                    if attr.name == "Date":
                        date = datetime.strptime(attr.get_value(), "%Y-%m-%d")
                        if date.strftime("%j") == today.strftime("%j"):
                            notice_json["today"]["notices"].append(data)
                            if notice.is_read is False:
                                notice_json["today"]["unread_count"] += 1
                        elif date.strftime("%V") == today.strftime("%V"):
                            notice_json["week"]["notices"].append(data)
                            if notice.is_read is False:
                                notice_json["week"]["unread_count"] += 1
                        elif int(date.strftime("%V")) == int(today.strftime("%V")) + 1:
                            notice_json["next_week"]["notices"].append(data)
                            if notice.is_read is False:
                                notice_json["next_week"]["unread_count"] += 1
                        elif int(date.strftime("%V")) > int(today.strftime("%V")) + 1:
                            notice_json["future"]["notices"].append(data)
                            if notice.is_read is False:
                                notice_json["future"]["unread_count"] += 1
        return notice_json

