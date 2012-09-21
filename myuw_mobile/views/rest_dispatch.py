from django.http import HttpResponse

class RESTDispatch:
    """ Handles passing on the request to the correct view method based on the request type.
    """
    def run(self, *args, **named_args):
        request = args[0]
        if "GET" == request.META['REQUEST_METHOD']:
            if hasattr(self, "GET"):
                return self.GET(*args, **named_args)
            else:
                return self.invalid_method(*args, **named_args)
        elif "POST" == request.META['REQUEST_METHOD']:
            if hasattr(self, "POST"):
                return self.POST(*args, **named_args)
            else:
                return self.invalid_method(*args, **named_args)
        elif "PUT" == request.META['REQUEST_METHOD']:
            if hasattr(self, "PUT"):
                return self.PUT(*args, **named_args)
            else:
                return self.invalid_method(*args, **named_args)
        elif "DELETE" == request.META['REQUEST_METHOD']:
            if hasattr(self, "DELETE"):
                return self.DELETE(*args, **named_args)
            else:
                return self.invalid_method(*args, **named_args)

        else:
            return self.invalid_method(*args, **named_args)

    def invalid_method(self, *args, **named_args):
        response = HttpResponse("Method not allowed")
        response.status_code = 405
        return response

    def invalid_session(self, *args, **named_args):
        response = HttpResponse('No valid userid in session')
        response.status_code = 400
        return response

    def data_not_found(self, *args, **named_args):
        response = HttpResponse('Data not found')
        response.status_code = 404
        return response
