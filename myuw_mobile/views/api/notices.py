from django.http import HttpResponse
import json
from myuw_mobile.views.rest_dispatch import RESTDispatch
from myuw_mobile.dao.notice import get_notices_for_current_user


class Notices(RESTDispatch):
    """
    Performs actions on resource at /api/v1/notices/.
    """

    def GET(self, request):
        """
        GET returns 200 with a list of notices for the current user
        """
        notices = get_notices_for_current_user()
        notice_json = self._get_json(notices)
        return HttpResponse(json.dumps(notice_json))



    def _get_json(self, notices):

        notice_json = {}
        for notice in notices:
            data = notice.json_data()
            data['id_hash'] = notice.id_hash
            data['is_read'] = notice.is_read
            if notice.custom_category in notice_json:
                notice_json[notice.custom_category]["notices"].append(data)
            else:
                notice_json[notice.custom_category] = {"notices": [data]}
        return notice_json