from myuw.dao.pws import get_regid_for_url_key
from myuw.dao.pws import get_idcard_photo
from django.http import HttpResponse, StreamingHttpResponse
from restclients.exceptions import DataFailureException


def show_photo(request, url_key):
    regid = get_regid_for_url_key(url_key)

    try:
        photo = get_idcard_photo(regid)
        return StreamingHttpResponse([photo.getvalue()],
                                     content_type="image/jpeg")
    except DataFailureException:
        response = HttpResponse()
        response.status = 404
        print "DFE"
    except Exception as ex:
        print "E: ", ex

    return response
