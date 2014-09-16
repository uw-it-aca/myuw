import logging
import json
from django.http import HttpResponse
from myuw_mobile.views.rest_dispatch import RESTDispatch
from myuw_mobile.dao.notice import get_notices_for_current_user, mark_notices_read_for_current_user
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

        # MYUW NOTICE REMOVAL
        # notices = get_notices_for_current_user()
        # notice_json = self._get_json(notices)
        # logger.debug(notice_json)
        # log_success_response(logger, timer)
        notice_json = []

        return HttpResponse(json.dumps(notice_json))



    def _get_json(self, notices):
        return self._get_json_for_date(notices, datetime.now())

    def _get_json_for_date(self, notices, today):
        notice_json = []

        for notice in notices:
            data = notice.json_data(include_abbr_week_month_day_format=True)
            data['id_hash'] = notice.id_hash
            data['is_read'] = notice.is_read
            data['category'] = notice.custom_category
            data['is_critical'] = notice.is_critical
            data['location_tags'] = notice.location_tags
            notice_json.append(data)
        return notice_json


    def PUT(self, request):
        notice_hashes = json.loads(request.body).get('notice_hashes', None)
        mark_notices_read_for_current_user(notice_hashes)
        return HttpResponse('')
