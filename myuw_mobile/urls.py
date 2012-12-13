from django.conf.urls import patterns, include, url
from myuw_mobile.views.page import index
from myuw_mobile.views.mobile_login import user_login
from myuw_mobile.views.support import support
from myuw_mobile.views.schedule_api import StudClasScheCurQuar, StudClasScheFutureQuar
from myuw_mobile.views.contact_api import InstructorContact
from myuw_mobile.views.textbook_api import TextbookCurQuar
from myuw_mobile.views.links_api import QuickLinks
from myuw_mobile.views.stud_finances_api import AccountBalances
from myuw_mobile.views.other_quarters_api import RegisteredFutureQuarters
from myuw_mobile.views.logout import Logout

urlpatterns = patterns('myuw_mobile.views',
    url(r'login', 'mobile_login.user_login'),
    url(r'support', 'support.support'),
    url(r'^visual', 'page.index'),
    url(r'^textbooks', 'page.index'),
    url(r'^future_quarters', 'page.index'),
    url(r'^next', 'page.index'),
    url(r'^instructor', 'page.index'),
    url(r'^links', 'page.index'),
    url(r'^finabala', 'page.index'),
    url(r'^final_exams', 'page.index'),
    url(r'^link/(?P<linkid>\d+)$', 'link.show_link'),
    url(r'^logger/(?P<interaction_type>\w+)$', 'logger.log_interaction'),
    url(r'logout', Logout.as_view()),
    url(r'^textbooks/(?P<year>\d{4}),(?P<quarter>[a-z]+)(?P<summer_term>[-,abterm]*)$', 'page.index'),
    url(r'^final_exams/(?P<year>\d{4}),(?P<quarter>[a-z]+)(?P<summer_term>[-,abterm]*)$', 'page.index'),
    url(r'^visual/(?P<year>\d{4}),(?P<quarter>[a-z]+)(?P<summer_term>[-,abterm]*)$', 'page.index'),
    url(r'^(?P<year>\d{4}),(?P<quarter>[a-z]+)(?P<summer_term>[-,abterm]*)$', 'page.index'),
    url(r'^$', 'page.index'),
    url(r'^api/v1/books/current/$', TextbookCurQuar().run),
#    url(r'^api/v1/book/(?P<year>\d{4}),(?P<quarter>[a-z]+)(?P<summer_term>[-,abterm]*)$',
#        TextbookFutureQuar().run),
    url(r'^api/v1/schedule/current/?$', StudClasScheCurQuar().run),
    url(r'^api/v1/schedule/(?P<year>\d{4}),(?P<quarter>[a-z]+)(?P<summer_term>[-,abterm]*)$',
        StudClasScheFutureQuar().run),
    url(r'^api/v1/links/$', QuickLinks().run),
    url(r'^api/v1/person/(?P<regid>.*)$', InstructorContact().run),
    url(r'^api/v1/finabala/$', AccountBalances().run),
    url(r'^api/v1/oquarters/$', RegisteredFutureQuarters().run),
)
