from django.http import HttpResponse
import json
from userservice.user import UserService

class RESTDispatch:
    """ Handles passing on the request to the correct view method based on the request type.
    """
    def run(self, *args, **named_args):
        request = args[0]

#        if not request.is_secure():
#            return insecure_connection()
        
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

def invalid_session():
    response = HttpResponse('No valid userid in session')
    response.status_code = 400
    return response

def invalid_arg():
    response = HttpResponse('No valid argument')
    response.status_code = 400
    return response

def data_not_found():
    response = HttpResponse('Data not found')
    response.status_code = 404
    return response

def invalid_method():
    response = HttpResponse("Method not allowed")
    response.status_code = 405
    return response

def insecure_connection():
    response = HttpResponse('HTTP to HTTPS')
    response.status_code = 497
    return response

