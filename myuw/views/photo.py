# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import StreamingHttpResponse
from myuw.dao.pws import get_regid_for_url_key
from myuw.dao.pws import get_idcard_photo
from restclients_core.exceptions import DataFailureException


@login_required
def show_photo(request, url_key):
    regid = get_regid_for_url_key(url_key)

    try:
        photo = get_idcard_photo(regid)
        return StreamingHttpResponse([photo.getvalue()],
                                     content_type="image/jpeg")
    except DataFailureException:
        return render(request, '404.html', status=404)
    except Exception as ex:
        return render(request, '543.html', status=500)
