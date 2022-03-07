# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from .base_settings import *
import sys
import os
import logging

ALLOWED_HOSTS += [
    'myuw.washington.edu',
    'myuw.uw.edu'
]

INSTALLED_APPS += [
    'uw_oidc',
    'compressor',
    'django_client_logger',
    'django_user_agents',
    'hx_toolkit',
    'rc_django',
    'userservice',
    'supporttools',
    'blti',
    'myuw.apps.MyUWConfig',
    'webpack_loader',
]

MIDDLEWARE.insert(3, 'uw_oidc.middleware.IDTokenAuthenticationMiddleware')

MIDDLEWARE += [
    'django.middleware.locale.LocaleMiddleware',
    'userservice.user.UserServiceMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'rc_django.middleware.EnableServiceDegradationMiddleware'
]

if os.getenv('AUTH', 'NONE') == 'SAML_MOCK':
    MOCK_SAML_ATTRIBUTES = {
        'uwnetid': ['javerage'],
        'affiliations': ['student', 'member', 'alum', 'staff', 'employee'],
        'eppn': ['javerage@washington.edu'],
        'scopedAffiliations': ['student@washington.edu',
                               'member@washington.edu'],
        'isMemberOf': ['u_test_group', 'u_test_another_group',
                       'u_astratest_myuw_test-support-admin'],
    }

# MYUW_PREFETCH_THREADING = True
MYUW_ENABLED_FEATURES = []

MYUWCLASS = "https://eo.admin.uw.edu/uweomyuw/myuwclass/uwnetid/myuwclass.asp?cid="

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = 587
EMAIL_TIMEOUT = 15
EMAIL_USE_TLS=True
EMAIL_SSL_CERTFILE = os.getenv('CERT_PATH', '')
EMAIL_SSL_KEYFILE = os.getenv('KEY_PATH', '')

MAILMAN_COURSEREQUEST_RECIPIENT = os.getenv("MAILMAN_REQUEST_RECIPIENT")
if os.getenv("ENV", "") == "prod":
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
else:
    EMAIL_BACKEND = "saferecipient.EmailBackend"
    SAFE_EMAIL_RECIPIENT = os.getenv("SAFE_EMAIL_RECIPIENT")

# uw_oidc settings
if os.getenv("ENV", "") == "dev":
    UW_TOKEN_ISSUER = "https://idp-eval.u.washington.edu"
    UW_TOKEN_SESSION_AGE = 600
else:
    UW_TOKEN_ISSUER = "https://idp.u.washington.edu"
    UW_TOKEN_SESSION_AGE = 3600
UW_TOKEN_AUDIENCE = "oidc/myuw"
UW_TOKEN_LEEWAY = 2
UW_OIDC_ENABLE_LOGGING = True

if os.getenv('SPACE_ENV') in ['PROD', 'EVAL']:
    RESTCLIENTS_SPACE_DAO_CLASS = 'Live'
    RESTCLIENTS_SPACE_CONNECT_TIMEOUT = 3
    RESTCLIENTS_SPACE_TIMEOUT = os.getenv("SPACE_TIMEOUT", 10)
    RESTCLIENTS_SPACE_POOL_SIZE = os.getenv("SPACE_POOL_SIZE", 10)
    RESTCLIENTS_SPACE_CERT_FILE = os.getenv('CERT_PATH', '')
    RESTCLIENTS_SPACE_KEY_FILE = os.getenv('KEY_PATH', '')
    if os.getenv('SPACE_ENV') == 'PROD':
        RESTCLIENTS_SPACE_HOST = 'https://ws.admin.washington.edu:443'
    else:
        RESTCLIENTS_SPACE_HOST = 'https://wseval.s.uw.edu:443'

# Thrive required settings
MEDIA_ROOT = "../statics/hx_images"
MEDIA_URL = "/uploaded_images/"
THRIVE_OUTPUT = "/hx_toolkit_output"
MYUW_DISABLE_ACTIONS_WHEN_OVERRIDE = False
MYUW_SKIP_ACCESS_CHECK = True

# dev/test site access settings
if os.getenv("ENV", "") == "localdev":
    MYUW_ASTRA_GROUP_STEM = "u_astratst_myuw"
    MYUW_ADMIN_GROUP = 'u_astratst_myuw_test-support-admin'
    MYUW_OVERRIDE_GROUP = 'u_astratst_myuw_test-support-impersonate'
else:
    MYUW_ASTRA_GROUP_STEM = "u_astra_myuw"
    MYUW_TEST_ACCESS_GROUP = "u_acadev_myuw-test-access"
    if os.getenv("ENV", "") == "prod":
        MYUW_ADMIN_GROUP = "u_astra_myuw_prod-support-admin"
        MYUW_OVERRIDE_GROUP = "u_astra_myuw_prod-support-impersonate"
        MYUW_DISABLE_ACTIONS_WHEN_OVERRIDE = True
    else:
        MYUW_ADMIN_GROUP = "u_astra_myuw_test-support-admin"
        MYUW_OVERRIDE_GROUP = "u_astra_myuw_test-support-impersonate"
        MYUW_SKIP_ACCESS_CHECK = False

# Support Tools settings
SUPPORTTOOLS_PARENT_APP = "MyUW"
SUPPORTTOOLS_PARENT_APP_URL = "/"

USERSERVICE_VALIDATION_MODULE = "myuw.authorization.validate_netid"
USERSERVICE_OVERRIDE_AUTH_MODULE = "myuw.authorization.can_override_user"
RESTCLIENTS_ADMIN_AUTH_MODULE = "myuw.authorization.can_proxy_restclient"

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = os.getenv("COMPRESSOR_ENABLED", "True") == "True"

if os.getenv("COMPRESSOR_ENABLED", "True") == "False":
    COMPRESS_ENABLED = False

COMPRESS_ROOT = "../static"
STATICFILES_FINDERS += (
    'compressor.finders.CompressorFinder',
)

TEMPLATES[0]['DIRS'] = ['/app/myuw/templates']
TEMPLATES[0]['OPTIONS']['context_processors'] += [
    'django.template.context_processors.i18n',
    'django.template.context_processors.media',
    'django.template.context_processors.static',
    'django.template.context_processors.tz',
    'supporttools.context_processors.supportools_globals',
    #'supporttools.context_processors.has_less_compiled',
    #'supporttools.context_processors.has_google_analytics',
    'myuw.context_processors.is_hybrid',
]

AWS_CA_BUNDLE = '/app/certs/ca-bundle.crt'
AWS_SQS = {
    'SECTION_STATUS_V1': {
        'QUEUE_ARN': os.getenv('SECTION_STATUS_QUEUE_ARN'),
        'KEY_ID': os.getenv('SECTION_STATUS_KEY_ID'),
        'KEY': os.getenv('SECTION_STATUS_KEY'),
        'VISIBILITY_TIMEOUT': 50,
        'MESSAGE_GATHER_SIZE': 10,
        'WAIT_TIME': 7,
        'VALIDATE_SNS_SIGNATURE': True,
        'PAYLOAD_SETTINGS': {}
    }
}

if os.getenv('MYPLAN_ENV') in RESTCLIENTS_DEFAULT_ENVS:
    RESTCLIENTS_MYPLAN_DAO_CLASS = 'Live'
    RESTCLIENTS_MYPLAN_CONNECT_TIMEOUT = 3
    RESTCLIENTS_MYPLAN_TIMEOUT = os.getenv("MYPLAN_TIMEOUT", 7)
    RESTCLIENTS_MYPLAN_POOL_SIZE = os.getenv(
        "MYPLAN_POOL_SIZE", RESTCLIENTS_DEFAULT_POOL_SIZE)
    RESTCLIENTS_MYPLAN_CERT_FILE = ''
    RESTCLIENTS_MYPLAN_KEY_FILE = ''
    RESTCLIENTS_MYPLAN_AUTH_SECRET = os.getenv('MYPLAN_AUTH_SECRET')
    if os.getenv('MYPLAN_ENV') == 'PROD':
        RESTCLIENTS_MYPLAN_HOST = 'https://api.planning.sis.uw.edu/'
    else:
        RESTCLIENTS_MYPLAN_HOST = 'https://api.planning-eval.sis.uw.edu/'


if os.getenv('MYPLAN_AUTH_ENV') in RESTCLIENTS_DEFAULT_ENVS:
    RESTCLIENTS_MYPLAN_AUTH_DAO_CLASS = 'Live'
    RESTCLIENTS_MYPLAN_AUTH_CONNECT_TIMEOUT = 3
    RESTCLIENTS_MYPLAN_AUTH_TIMEOUT = 10
    RESTCLIENTS_MYPLAN_AUTH_POOL_SIZE = 3
    if os.getenv('MYPLAN_AUTH_ENV') == 'PROD':
        RESTCLIENTS_MYPLAN_AUTH_HOST = 'https://auth.api.planning.sis.uw.edu:443'
    else:
        RESTCLIENTS_MYPLAN_AUTH_HOST = 'https://auth.api.planning-eval.sis.uw.edu:443'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'stdout_stream': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': lambda record: record.levelno < logging.WARN
        },
        'stderr_stream': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': lambda record: record.levelno > logging.INFO
        }
    },
    'formatters': {
        'myuw': {
            'format': '%(name)s %(levelname)-4s %(asctime)s %(message)s',
        },
    },
    'handlers': {
        'stdout': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'filters': ['stdout_stream'],
            'formatter': 'myuw',
        },
        'stderr': {
            'class': 'logging.StreamHandler',
            'stream': sys.stderr,
            'filters': ['stderr_stream'],
            'formatter': 'myuw',
        },
    },
    'loggers': {
        '': {
            'handlers': ['stdout', 'stderr'],
            'level': 'INFO' if os.getenv('ENV', 'dev') == 'prod' else 'DEBUG'
        }
    }
}

DEBUG = False
if os.getenv("ENV", '') == "localdev":
    DEBUG = True
    MEMCACHED_SERVERS=['localhost:11211']
else:
    RESTCLIENTS_DAO_CACHE_CLASS = 'myuw.util.cache.MyUWMemcachedCache'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
GOOGLE_ANALYTICS_KEY = os.getenv('GOOGLE_ANALYTICS_KEY', None)
GOOGLE_SEARCH_KEY = os.getenv('GOOGLE_SEARCH_KEY', None)

# Location of stats file that can be accessed during local development and 
# collected from during production build process

if os.getenv("ENV") == "localdev":
    WEBPACK_LOADER = {
        'DEFAULT': {
            'STATS_FILE': os.path.join(BASE_DIR, 'myuw/static/webpack-stats.json'),
        }
    }
else:
    WEBPACK_LOADER = {
        'DEFAULT': {
            'STATS_FILE': '/static/webpack-stats.json',
        }
    }
