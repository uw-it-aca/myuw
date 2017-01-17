from myuw.util.thread import PrefetchThread
from myuw.dao.affiliation import affiliation_prefetch
from myuw.dao.enrollment import enrollment_prefetch
from myuw.dao.library import library_resource_prefetch
from myuw.dao.password import password_prefetch
from myuw.dao.pws import person_prefetch
from myuw.dao.term import current_terms_prefetch
from myuw.dao.uwemail import index_forwarding_prefetch


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


def prefetch_resources(request):
    prefetch_methods = []
    prefetch_methods.extend(person_prefetch())
    prefetch_methods.extend(index_forwarding_prefetch())
    prefetch_methods.extend(current_terms_prefetch(request))
    prefetch_methods.extend(enrollment_prefetch())
    prefetch_methods.extend(affiliation_prefetch())
    prefetch_methods.extend(password_prefetch())
    prefetch_methods.extend(library_resource_prefetch())

    prefetch(request, prefetch_methods)
