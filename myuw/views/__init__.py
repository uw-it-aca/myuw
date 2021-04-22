# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django import template
from myuw.dao.enrollment import enrollment_prefetch
from myuw.dao.library import library_resource_prefetch
from myuw.dao.gws import group_prefetch
from myuw.dao.instructor import is_instructor_prefetch
from myuw.dao.pws import person_prefetch
from myuw.dao.password import password_prefetch
from myuw.dao.student_profile import sws_person_prefetch
from myuw.dao.term import current_terms_prefetch
from myuw.dao.uwnetid import subscriptions_prefetch
from myuw.dao.canvas import canvas_prefetch
from myuw.dao.user_pref import migration_preference_prefetch
from myuw.util.settings import get_enabled_features
from myuw.util.thread import PrefetchThread


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
                       prefetch_migration_preference=False,
                       prefetch_enrollment=False,
                       prefetch_group=False,
                       prefetch_instructor=False,
                       prefetch_library=False,
                       prefetch_password=False,
                       prefetch_canvas=False,
                       prefetch_sws_person=False):
    """
    Common resource prefetched: affiliation, term
    """
    prefetch_methods = []
    prefetch_methods.extend(current_terms_prefetch(request))
    prefetch_methods.extend(person_prefetch())
    prefetch_methods.extend(subscriptions_prefetch())

    if prefetch_migration_preference:
        prefetch_methods.extend(migration_preference_prefetch())

    if prefetch_instructor:
        # depends on person
        prefetch_methods.extend(is_instructor_prefetch())

    if prefetch_enrollment:
        # depends on pws.person
        prefetch_methods.extend(enrollment_prefetch())

    if prefetch_group:
        prefetch_methods.extend(group_prefetch())

    if prefetch_library:
        prefetch_methods.extend(library_resource_prefetch())

    if prefetch_canvas:
        # depends on pws.person
        prefetch_methods.extend(canvas_prefetch())

    if prefetch_password:
        prefetch_methods.extend(password_prefetch())

    if prefetch_sws_person:
        prefetch_methods.extend(sws_person_prefetch())

    prefetch(request, prefetch_methods)


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
