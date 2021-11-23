import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/myuw>`_.
"""

# The VERSION file is created by travis-ci, based on the tag name
version_path = 'myuw/VERSION'
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

url = "https://github.com/uw-it-aca/myuw"
setup(
    name='MyUW',
    version=VERSION,
    packages=['myuw'],
    author="UW-IT AXDD",
    author_email="aca-it@uw.edu",
    include_package_data=True,
    install_requires=[
        'Django~=2.2',
        'ordereddict',
        'beautifulsoup4',
        'urllib3',
        'uw-memcached-clients~=1.0.9',
        'UW-Django-SAML2~=1.5',
        'aws-message-client~=1.5',
        'UW-RestClients-Core==1.3.8',
        'UW-RestClients-Bookstore~=1.1',
        'UW-RestClients-Canvas~=1.2',
        'UW-RestClients-CoDa~=1.0',
        'UW-RestClients-Grad~=1.1',
        'UW-RestClients-GradePage~=1.2',
        'UW-RestClients-GWS~=2.3',
        'UW-RestClients-HFS~=1.0.4',
        'UW-RestClients-IASystem~=1.1',
        'UW-RestClients-Libraries~=1.3',
        'UW-RestClients-Mailman~=1.0',
        'UW-RestClients-MyPlan~=1.0.1',
        'UW-RestClients-PWS~=2.1.4',
        'UW-RestClients-SWS==2.3.15',
        'UW-RestClients-Sdbmyuw~=1.0',
        'UW-RestClients-Space>1.0',
        'UW-RestClients-Trumba~=1.3.6',
        'UW-RestClients-UPass~=1.0.1',
        'UW-RestClients-UWNetID~=1.0.7',
        'django-userservice~=3.1',
        'UW-RestClients-Django-Utils~=2.3',
        'Uw-Django-Oidc<1.0',
        'Django-SupportTools~=3.5',
        'Django-Safe-EmailBackend~=1.2',
        'django_client_logger<3.0',
        'UW-HX-Toolkit~=2.6',
        'django-blti~=2.2',
        'bleach',
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
        'Programming Language :: Python :: 3.6',
    ],
)
