from django.conf.urls import include, url


urlpatterns = [
    url(r'^support', include('userservice.urls')),
    url(r'^logging', include('rc_django.urls')),
    url(r'^logging', include('django_client_logger.urls')),
    url(r'^logging', include('rc_django.urls')),
    url(r'^', include('myuw.urls')),
]
