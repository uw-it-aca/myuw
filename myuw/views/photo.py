from myuw.dao.pws import get_regid_for_url_key
from myuw.dao.pws import get_idcard_photo
from myuw.views.rest_dispatch import data_error, data_not_found
from django.http import HttpResponse, StreamingHttpResponse
from restclients.exceptions import DataFailureException


def show_photo(request, url_key):
    regid = get_regid_for_url_key(url_key)

    try:
        photo = get_idcard_photo(regid)
        return StreamingHttpResponse([photo.getvalue()],
                                     content_type="image/jpeg")
    except DataFailureException:
        return data_not_found()
    except Exception as ex:
        return data_error()
