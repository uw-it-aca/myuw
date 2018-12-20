from .base_settings import *

ALLOWED_HOSTS = ['*']


INSTALLED_APPS += [
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

MIDDLEWARE += [
    'userservice.user.UserServiceMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware'
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


