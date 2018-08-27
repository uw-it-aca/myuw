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
        'Django==1.11.10',
        'ordereddict',
        'simplejson',
        'django-compressor==2.2',
        'beautifulsoup4',
        'urllib3==1.23',
        'django-templatetag-handlebars',
        'django_client_logger>=1.2,<2.0',
        'django-blti==0.6',
        'unittest2',
        'UW-Django-SAML2>=0.4.5,<1.0',
        'django-aws-message>=1.0,<2.0',
        'UW-RestClients-Core==0.9.6',
        'UW-RestClients-Bookstore>=0.5.3',
        'UW-RestClients-Canvas>=0.7.2,<1.0',
        'UW-RestClients-CoDa',
        'UW-RestClients-Grad<2.0,>=1.0',
        'UW-RestClients-GradePage<1.0,>=0.1.1',
        'UW-RestClients-GWS>=1.0,<2.0',
        'UW-RestClients-Mailman>=0.2.1,<1.0',
        'UW-RestClients-MyPlan<1.0',
        'UW-RestClients-HFS<1.0',
        'UW-RestClients-IASystem>=0.3.1,<1.0',
        'UW-RestClients-Libraries<1.0',
        'UW-RestClients-PWS<2.0,>=1.0.1',
        'UW-RestClients-SWS<2.0,>=1.7.3',
        'UW-RestClients-Trumba<1.0,>=0.3',
        'UW-RestClients-UPass>=0.2,<1.0',
        'UW-RestClients-UWNetID>=0.8,<1.0',
        'UW-RestClients-Sdbmyuw',
        'UW-RestClients-Django-Utils>=1.4,<2.0',
        'django-userservice>=2.0.2,<3.0',
        'Django-SupportTools>=2.0.4,<3.0',
        'Django-Safe-EmailBackend>=0.1,<1.0',
        'UW-HX-Toolkit==1.04',
        'django_mobileesp',
        'yajl',
        'bleach',
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
        'Programming Language :: Python :: 2.7',
    ],
)
