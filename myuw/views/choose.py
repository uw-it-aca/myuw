from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from myuw.models import UserMigrationPreference
from myuw.dao.pws import get_netid_of_current_user
from userservice.user import UserService
from myuw.views.page import redirect_to_legacy_site


@login_required
def new_site(request):
    username = get_netid_of_current_user()
    obj, x = UserMigrationPreference.objects.get_or_create(username=username)
    obj.use_legacy_site = False
    obj.save()

    return HttpResponseRedirect(reverse("myuw_home"))


@login_required
def old_site(request):
    if "POST" == request.method:
        username = get_netid_of_current_user()
        get_or_create = UserMigrationPreference.objects.get_or_create
        obj, is_new = get_or_create(username=username)
        obj.use_legacy_site = True
        obj.save()

    return redirect_to_legacy_site()
