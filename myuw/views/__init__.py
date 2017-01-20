from myuw.util.thread import PrefetchThread
from myuw.dao.affiliation import affiliation_prefetch
from myuw.dao.enrollment import enrollment_prefetch
from myuw.dao.library import library_resource_prefetch
from myuw.dao.password import password_prefetch
from myuw.dao.pws import person_prefetch
from myuw.dao.term import current_terms_prefetch
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
                       prefetch_canvas=False):
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

    prefetch(request, prefetch_methods)
