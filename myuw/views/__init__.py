from django.conf import settings
from django import template
from django.shortcuts import render
from myuw.util.thread import PrefetchThread
from myuw.dao.affiliation import affiliation_prefetch
from myuw.dao.enrollment import enrollment_prefetch
from myuw.dao.library import library_resource_prefetch
from myuw.dao.password import password_prefetch
from myuw.dao.pws import person_prefetch
from myuw.dao.gws import is_in_admin_group
from myuw.dao.term import current_terms_prefetch
from myuw.dao.upass import upass_prefetch
from myuw.dao.uwemail import email_forwarding_prefetch
from myuw.dao.canvas import canvas_prefetch


def prefetch(request, prefetch_methods):
    prefetch_threads = []
    for method in prefetch_methods:
        thread = PrefetchThread()
        thread.method = method
        thread.request = request
        thread.start()
        prefetch_threads.append(thread)

    for i in range(len(prefetch_threads)):
        thread = prefetch_threads[i]
        thread.join()


def prefetch_resources(request,
                       prefetch_email=False,
                       prefetch_enrollment=False,
                       prefetch_library=False,
                       prefetch_password=False,
                       prefetch_person=False,
                       prefetch_canvas=False,
                       prefetch_upass=False):
    """
    Common resource prefetched: affiliation, term
    """
    prefetch_methods = []
    prefetch_methods.extend(affiliation_prefetch())
    prefetch_methods.extend(current_terms_prefetch(request))

    if prefetch_email:
        prefetch_methods.extend(email_forwarding_prefetch())

    if prefetch_enrollment:
        prefetch_methods.extend(enrollment_prefetch())

    if prefetch_library:
        prefetch_methods.extend(library_resource_prefetch())

    if prefetch_password:
        prefetch_methods.extend(password_prefetch())

    if prefetch_person:
        prefetch_methods.extend(person_prefetch())

    if prefetch_canvas:
        prefetch_methods.extend(canvas_prefetch())

    if prefetch_upass:
        prefetch_methods.extend(upass_prefetch())

    prefetch(request, prefetch_methods)


def get_enabled_features():
    return getattr(settings, "MYUW_ENABLED_FEATURES", [])


def admin_required(group_key):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            is_admin = is_in_admin_group(group_key)
            if is_admin is False:
                return render(request, 'no_access.html', {})

            return func(request, *args, **kwargs)

        return wrapper
    return decorator


def set_admin_wrapper_template(context):
    try:
        extra_template = "userservice/user_override_extra_info.html"
        template.loader.get_template(extra_template)
        context['has_extra_template'] = True
        context['extra_template'] = 'userservice/user_override_extra_info.html'
    except template.TemplateDoesNotExist:
        # This is a fine exception - there doesn't need to be an extra info
        # template
        pass

    try:
        template.loader.get_template("userservice/user_override_wrapper.html")
        context['wrapper_template'] = 'userservice/user_override_wrapper.html'
    except template.TemplateDoesNotExist:
        context['wrapper_template'] = 'support_wrapper.html'
        # This is a fine exception - there doesn't need to be an extra info
        # template
        pass
