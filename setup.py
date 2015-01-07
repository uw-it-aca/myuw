#!/usr/bin/env python

from distutils.core import setup

setup(name='MyUW',
      version='4.0',
      description='',
      install_requires=[
         'Django==1.6',
         'South',
         'ordereddict',
         'simplejson',
         'django-compressor',
         'BeautifulSoup',
         'urllib3',
         'django-templatetag-handlebars',
         'AuthZ-Group==1.1.2',
         'Django-UserService==1.0.2',
         'unittest2',
         'django_mobileesp',
         'RestClients',
         'SupportTools',
         'PermissionsLogging',
         'django_client_logger',
        ],
      dependency_links=[
         'git+https://github.com/abztrakt/django-mobileesp.git#egg=django_mobileesp-dev',
         'git+https://github.com/uw-it-aca/uw-restclients.git#egg=RestClients-dev',
         'git+https://github.com/abztrakt/django-mobileesp.git#egg=django_mobileesp-dev',
         'git+https://github.com/uw-it-aca/django-supporttools.git#egg=SupportTools-dev',
         'git+https://github.com/vegitron/permissions_logging.git#egg=PermissionsLogging-dev',
         'git+https://github.com/devights/django_client_logger.git#egg=django_client_logger-dev',
      ],
     )
