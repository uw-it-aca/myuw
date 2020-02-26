import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

DEBUG = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'uw_oidc',
    'django_user_agents',
    'compressor',
    'django_client_logger',
    'userservice',
    'rc_django',
    'supporttools',
    'blti',
    'hx_toolkit',
    'myuw.apps.MyUWConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'uw_oidc.middleware.IDTokenAuthenticationMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.PersistentRemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'userservice.user.UserServiceMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'rc_django.middleware.EnableServiceDegradationMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.RemoteUserBackend',
#    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'travis-ci.urls'

WSGI_APPLICATION = 'travis-ci.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = 'static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

COMPRESS_ENABLED = False
COMPRESS_ROOT = "compress_root"

# EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
EMAIL_BACKEND = "saferecipient.EmailBackend"

MEDIA_ROOT = "/statics/hx_images"
MEDIA_URL = "/uploaded_images/"
THRIVE_OUTPUT = "/hx_toolkit_output"

MYUW_ENABLED_FEATURES = []

RESTCLIENTS_TEST_MEMCACHED = True
RESTCLIENTS_MEMCACHED_SERVERS = ('localhost:11211', )
USER_AGENTS_CACHE = None

USERSERVICE_VALIDATION_MODULE = "myuw.authorization.validate_netid"
USERSERVICE_OVERRIDE_AUTH_MODULE = "myuw.authorization.can_override_user"
RESTCLIENTS_ADMIN_AUTH_MODULE = "myuw.authorization.can_proxy_restclient"

MOCK_SAML_ATTRIBUTES = {
    'uwnetid': ['javerage'],
    'affiliations': ['student', 'member', 'alum', 'staff', 'employee'],
    'eppn': ['javerage@washington.edu'],
    'scopedAffiliations': ['student@washington.edu', 'member@washington.edu'],
    'isMemberOf': ['u_test_group', 'u_test_another_group',
                   'u_astratest_myuw_test-support-admin'],
}

from django.urls import reverse_lazy
LOGIN_URL = reverse_lazy('saml_login')
LOGOUT_URL = reverse_lazy('saml_logout')

REMOTE_USER_FORMAT = "uwnetid"
