from userservice.user import UserService
from myuw.util.performance import log_response_time
from myuw.views.error import invalid_method


class RESTDispatch(object):
    """
    Handles passing on the request to the correct view
    method based on the request type.
    """
    @log_response_time
    def run(self, *args, **named_args):
        request = args[0]

        user_service = UserService()
        netid = user_service.get_user()
        if not netid:
            return invalid_session()

        if "GET" == request.META['REQUEST_METHOD']:
            if hasattr(self, "GET"):
                return self.GET(*args, **named_args)
            else:
                return invalid_method()
        elif "POST" == request.META['REQUEST_METHOD']:
            if hasattr(self, "POST"):
                return self.POST(*args, **named_args)
            else:
                return invalid_method()
        elif "PUT" == request.META['REQUEST_METHOD']:
            if hasattr(self, "PUT"):
                return self.PUT(*args, **named_args)
            else:
                return invalid_method()
        elif "DELETE" == request.META['REQUEST_METHOD']:
            if hasattr(self, "DELETE"):
                return self.DELETE(*args, **named_args)
            else:
                return invalid_method()

        else:
            return invalid_method()
