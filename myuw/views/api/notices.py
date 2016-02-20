import logging
import json
import traceback
from datetime import datetime
from django.http import HttpResponse
from myuw.dao.notice import get_notices_for_current_user
from myuw.dao.notice import mark_notices_read_for_current_user
from myuw.dao.notice_mapping import get_json_for_notices
from myuw.logger.timer import Timer
from myuw.logger.logresp import log_success_response, log_err
from myuw.views.rest_dispatch import RESTDispatch, data_error


logger = logging.getLogger(__name__)


class Notices(RESTDispatch):
    """
    Performs actions on resource at /api/v1/notices/.
    """
    def GET(self, request):
        """
        GET returns 200 with a list of notices for the current user
        """
        timer = Timer()
        try:
            notice_json = get_json_for_notices(
                request, get_notices_for_current_user())
            log_success_response(logger, timer)
            return HttpResponse(json.dumps(notice_json))
        except Exception:
            log_err(logger, timer, traceback.format_exc())
            return data_error()

    def _get_json(self, notices):
        return self._get_json_for_date(notices, datetime.now())

    def _get_json_for_date(self, notices, today):
        notice_json = []

        for notice in notices:
            data = notice.json_data(include_abbr_week_month_day_format=True)
            data['id_hash'] = notice.id_hash
            data['is_read'] = notice.is_read
            data['category'] = notice.custom_category
            data['myuw_id'] = notice.notice_typecustom_category
            data['is_critical'] = notice.is_critical
            data['location_tags'] = notice.location_tags
            notice_json.append(data)
        return _associate_short_to_long(notice_json)

    def PUT(self, request):
        notice_hashes = json.loads(request.body).get('notice_hashes', None)
        mark_notices_read_for_current_user(notice_hashes)
        return HttpResponse('')
