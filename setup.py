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
        'Django==1.10.5',
        'ordereddict',
        'simplejson',
        'django-compressor',
        'BeautifulSoup',
        'urllib3==1.10.2',
        'django-templatetag-handlebars',
        'django-userservice==1.2.1',
        'unittest2',
        'AuthZ-Group',
        'python-binary-memcached',
        'UW-RestClients-Core==0.9.2a1',
        'UW-RestClients-SWS<2.0,>=1.4.3',
        'UW-RestClients-PWS<1.0,>=0.6',
        'UW-RestClients-HFS<1.0',
        'UW-RestClients-GWS<1.0',
        'UW-RestClients-GradePage<1.0,>=0.1.1',
        'UW-RestClients-Libraries<1.0',
        'UW-RestClients-IASystem<1.0,>=0.1.5',
        'UW-RestClients-Canvas<1.0,>=0.6.4',
        'UW-RestClients-UPass<1.0',
        'UW-RestClients-UWNetID<1.0',
        'UW-RestClients-Grad<1.0',
        'UW-RestClients-Bookstore<1.0',
        'UW-RestClients-Mailman<1.0',
        'UW-RestClients-MyPlan<1.0',
        'UW-RestClients-Trumba<1.0,>=0.3',
        'UW-RestClients-Django-Utils<1.0',
        'Django-SupportTools',
        'django_mobileesp',
        'django_client_logger',
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
