import simplejson as json
import re
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from myuw.util.performance import log_response_time
from myuw.views import prefetch_resources

SPACE_PATTERN = r'%20'
AMP_PATTERN = r'%26'


def unescape_curriculum_abbr(cur_abb):
    if re.search(SPACE_PATTERN, cur_abb):
        cur_abb = re.sub(SPACE_PATTERN, ' ', cur_abb)
    if re.search(AMP_PATTERN, cur_abb):
        cur_abb = re.sub(AMP_PATTERN, '&', cur_abb)
    return cur_abb


def json_serializer(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()


@method_decorator(log_response_time, name='dispatch')
class OpenAPI(View):
    """
    Default MyUW API class, does not require AuthN.
    """
    def json_response(self, content='', status=200):
        return HttpResponse(json.dumps(content, default=json_serializer),
                            status=status,
                            content_type='application/json')

    def html_response(self, content='', status=200):
        return HttpResponse(content,
                            status=status,
                            content_type='text/html')


@method_decorator(login_required, name='dispatch')
class ProtectedAPI(OpenAPI):
    """
    Protected MyUW API class that adds login AuthN requirement.
    """
    pass
