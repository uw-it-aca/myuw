from .base_settings import *
import sys
import os

ALLOWED_HOSTS = ['*']

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
    'myuw.apps.MyUWConfig'
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

# Thrive required settings
MEDIA_ROOT = "/statics/hx_images"
MEDIA_URL = "/uploaded_images/"
THRIVE_OUTPUT = "/hx_toolkit_output"

# dev/test site access settings
if os.getenv("ENV", "") == "localdev":
    MYUW_ASTRA_GROUP_STEM = "u_astratst_myuw"
    MYUW_ADMIN_GROUP = 'u_astratst_myuw_test-support-admin'
    MYUW_OVERRIDE_GROUP = 'u_astratst_myuw_test-support-impersonate'
    MYUW_SKIP_ACCESS_CHECK = True
else:
    MYUW_ASTRA_GROUP_STEM = "u_astra_myuw"
    MYUW_TEST_ACCESS_GROUP = "u_acadev_myuw-test-access"
    if os.getenv("ENV", "") == "prod":
        MYUW_ADMIN_GROUP = "u_astra_myuw_prod-support-admin"
        MYUW_OVERRIDE_GROUP = "u_astra_myuw_prod-support-impersonate"
        MYUW_DISABLE_ACTIONS_WHEN_OVERRIDE = True
        MYUW_SKIP_ACCESS_CHECK = True
    else:
        MYUW_ADMIN_GROUP = "u_astra_myuw_test-support-admin"
        MYUW_OVERRIDE_GROUP = "u_astra_myuw_test-support-impersonate"
        MYUW_DISABLE_ACTIONS_WHEN_OVERRIDE = False
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

COMPRESS_ROOT = "/static"
STATICFILES_FINDERS += (
    'compressor.finders.CompressorFinder',
)

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

TEMPLATES[0]['DIRS'] = ['/app/myuw/templates']
TEMPLATES[0]['OPTIONS']['context_processors'] += [
    'django.template.context_processors.i18n',
    'django.template.context_processors.media',
    'django.template.context_processors.static',
    'django.template.context_processors.tz',
    'supporttools.context_processors.supportools_globals',
    'supporttools.context_processors.has_less_compiled',
    'supporttools.context_processors.has_google_analytics',
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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'stdout_stream': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': lambda record: record.levelno <= logging.WARNING
        },
        'stderr_stream': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': lambda record: record.levelno >= logging.ERROR
        }
    },
    'formatters': {
        'myuw': {
            'format': '%(name)s %(levelname)-4s %(asctime)s %(message)s',
        },
        'pref': {
            'format': 'pref:%(name)s %(levelname)-4s %(asctime)s %(message)s',
        },
        'event': {
            'format': 'event:%(name)s %(levelname)-4s %(asctime)s %(message)s',
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
        'pref': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'filters': ['stdout_stream'],
            'formatter': 'pref',
        },
        'event': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'filters': ['stdout_stream'],
            'formatter': 'event',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
        'django.request': {
            'handlers': ['stderr'],
            'level': 'ERROR',
            'propagate': True,
        },
        'myuw.views.api.banner_message': {
            'handlers': ['pref'],
            'level': 'INFO',
            'propagate': False,
        },
        'myuw.views.api.resources.pin': {
            'handlers': ['pref'],
            'level': 'INFO',
            'propagate': False,
        },
        'myuw.views.api.instructor_section_display': {
            'handlers': ['pref'],
            'level': 'INFO',
            'propagate': False,
        },
        'aws_message': {
            'handlers': ['event'],
            'level': 'INFO',
            'propagate': False,
        },
        'myuw.event': {
            'handlers': ['event'],
            'level': 'INFO',
            'propagate': False,
        },
        'myuw.management.commands.load_section_status_changes': {
            'handlers': ['event'],
            'level': 'INFO',
            'propagate': False,
        },
        '': {
            'handlers': ['stdout', 'stderr'],
            'level': 'DEBUG' if os.getenv('ENV', '') == 'dev' else 'INFO'
        }
    }
}


if os.getenv("ENV", '') == "localdev":
    DEBUG = True
else:
    RESTCLIENTS_DAO_CACHE_CLASS = 'myuw.util.cache_implementation.MyUWMemcachedCache'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
GOOGLE_ANALYTICS_KEY = os.getenv('GOOGLE_ANALYTICS_KEY', None)
GOOGLE_SEARCH_KEY = os.getenv('GOOGLE_SEARCH_KEY', None)
