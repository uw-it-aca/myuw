# Copyright 2026 uw-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import os
from setuptools import setup

README = """
See the README on `GitHub <https://github.com/uw-it-aca/myuw>`_.
"""

# The VERSION file is created by travis-ci, based on the tag name
version_path = 'myuw/VERSION'
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace('\n', '')

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

url = 'https://github.com/uw-it-aca/myuw'
setup(
    name='MyUW',
    version=VERSION,
    packages=['myuw'],
    author='UWIT Student & Educational Technology Services',
    author_email='aca-it@uw.edu',
    include_package_data=True,
    install_requires=[
        'django~=5.2',
        'ordereddict',
        'beautifulsoup4',
        'urllib3',
        'uw-memcached-clients~=1.1',
        'uw-django-saml2~=1.8',
        'django-userservice~=3.2',
        'aws-message-client~=1.6',
        'uw-restclients-core~=1.4',
        'uw-restclients-bookstore~=1.4',
        'uw-restclients-canvas~=1.2',
        'uw-restclients-coda~=1.0',
        'uw-restclients-grad~=1.1',
        'uw-restclients-gradepage~=1.2',
        'uw-restclients-gws~=2.3',
        'uw-restclients-hfs~=1.0',
        'uw-restclients-iasystem~=1.1',
        'uw-restclients-libraries~=1.3',
        'uw-restclients-mailman~=2.1',
        'uw-restclients-myplan~=1.3',
        'uw-restclients-pws~=2.1',
        'uw-restclients-sws~=2.5',
        'uw-restclients-sdbmyuw~=1.0',
        'uw-restclients-space~=1.2',
        'uw-restclients-sps-contacts~=1.0',
        'uw-restclients-trumba~=1.4',
        'uw-restclients-upass~=4.0',
        'uw-restclients-uwnetid~=1.1',
        'uw-django-oidc~=1.0',
        'django-supporttools~=3.6',
        'django-persistent-message~=1.3',
        'uw-restclients-django-utils~=2.3',
        'django-safe-emailbackend~=1.2',
        'django_client_logger~=3.1',
        'nh3',
        'pyyaml',
        'ua-parser',
        'user-agents',
        'django-user-agents',
        'django-webpack-loader==1.4.0',
        'django-compressor',
    ],
    license='Apache License, Version 2.0',
    description=('MyUW is the portal of the University of Washington'),
    long_description=README,
    url=url,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
