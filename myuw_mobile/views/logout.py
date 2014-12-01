from django.views.generic import View
from django.http import HttpResponseRedirect


class Logout(View):
    def post(self, request):
        request.session.flush()

        return HttpResponseRedirect("/mobile/user_logout")

    def get(self, request):
        return HttpResponseRedirect("/mobile/")
