import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

DEBUG = True
ALLOWED_HOSTS = ['*']


<<<<<<< HEAD
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_user_agents',
    'compressor',
    'rc_django',
    'templatetag_handlebars',
    'myuw',
    'userservice',
    'django_client_logger',
    'supporttools',
    'blti',
    'hx_toolkit'
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'userservice.user.UserServiceMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware'
]


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.RemoteUserBackend',
]

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'
RESTCLIENTS_MEMCACHED_SERVERS = ('localhost:11211')

import os
if os.getenv('DB', "sqlite3") == "sqlite3":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
elif os.getenv('DB', "sqlite3") == "mysql":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'HOST': os.getenv("RDS_HOSTNAME", "localhost"),
            'NAME': os.getenv("RDS_DB_NAME", "myuw"),
            'USER': os.getenv("RDS_USERNAME", "myuw"),
            'PASSWORD': os.getenv("RDS_PASSWORD", "my_pass"),
        }
    }


if os.getenv('CACHE', "none") == "memcached":
    RESTCLIENTS_DAO_CACHE_CLASS='myuw.util.cache_implementation.MyUWMemcachedCache'
    RESTCLIENTS_MEMCACHED_SERVERS = (os.getenv('CACHE_NODE_0', "") + ":" + os.getenv('CACHE_PORT', "11211"), os.getenv('CACHE_NODE_1', "") + ":" + os.getenv('CACHE_PORT', "11211"),)

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

COMPRESS_ENABLED = False
COMPRESS_ROOT = "/static/"
STATIC_ROOT = "/static/"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'debug':  True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }
    }
]
# MYUW_PREFETCH_THREADING = True
MYUW_ENABLED_FEATURES = []

EMAIL_BACKEND = "saferecipient.EmailBackend"
MAILMAN_COURSEREQUEST_RECIPIENT = ""


# Thrive required settings
MEDIA_ROOT = "/statics/hx_images"
MEDIA_URL = "/uploaded_images/"
THRIVE_OUTPUT = "/hx_toolkit_output"

USERSERVICE_VALIDATION_MODULE = "myuw.authorization.validate_netid"
USERSERVICE_OVERRIDE_AUTH_MODULE = "myuw.authorization.can_override_user"
RESTCLIENTS_ADMIN_AUTH_MODULE = "myuw.authorization.can_proxy_restclient"
MYUW_ADMIN_GROUP = 'u_astratst_myuw_test-support-admin'
MYUW_OVERRIDE_GROUP = 'u_astratst_myuw_test-support-impersonate'
MYUW_ASTRA_GROUP_STEM = "u_astratst_myuw"
MYUW_DISABLE_ACTIONS_WHEN_OVERRIDE = False

#Support Tools settings
SUPPORTTOOLS_PARENT_APP = "MyUW"
SUPPORTTOOLS_PARENT_APP_URL = "/"

REMOTE_USER_FORMAT = "uwnetid"

MOCK_SAML_ATTRIBUTES = {
    'uwnetid': ['javerage'],
    'affiliations': ['student', 'member', 'alum', 'staff', 'employee'],
    'eppn': ['javerage@washington.edu'],
    'scopedAffiliations': ['student@washington.edu', 'member@washington.edu'],
    'isMemberOf': ['u_test_group', 'u_test_another_group',
                   'u_astratest_myuw_test-support-admin'],
}

from django.core.urlresolvers import reverse_lazy
LOGIN_URL = reverse_lazy('saml_login')

LOGOUT_URL = reverse_lazy('saml_logout')
