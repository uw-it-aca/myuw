from myuw.views.error import data_error
class ExceptionLogMiddleware(object):

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        return request

    def process_exception(self, request, exception):
        print 'EX'
        return data_error()
