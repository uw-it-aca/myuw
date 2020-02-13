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
        'Django>=2.0.10,<2.1',
        'ordereddict',
        'django-compressor==2.2',
        'beautifulsoup4',
        'urllib3>1.24',
        'python-dateutil',
        'Uw-Django-Oidc<1.0',
        'UW-Django-SAML2<2.0',
        'django-aws-message>=1.5.1,<2.0',
        'UW-RestClients-Core>=1.2.1,<2.0',
        'UW-RestClients-Bookstore>=1.0.4,<2.0',
        'UW-RestClients-Canvas>=1.1.8,<2.0',
        'UW-RestClients-CoDa<2.0',
        'UW-RestClients-Grad<2.0',
        'UW-RestClients-GradePage<2.0',
        'UW-RestClients-GWS>=2.2.5,<3.0',
        'UW-RestClients-HFS<2.0',
        'UW-RestClients-IASystem>=1.1,<2.0',
        'UW-RestClients-Libraries<2.0',
        'UW-RestClients-Mailman<2.0',
        'UW-RestClients-MyPlan<2.0',
        'UW-RestClients-PWS==2.0.5',
        'UW-RestClients-SWS>=2.2.6,<3.0',
        'UW-RestClients-Sdbmyuw<2.0',
        'UW-RestClients-Trumba<2.0',
        'UW-RestClients-UPass<2.0',
        'UW-RestClients-UWNetID<2.0',
        'Django-Template-Preprocess>=1.0.2,<2.0',
        'django-userservice<4.0',
        'UW-RestClients-Django-Utils>=2.1.5,<3.0',
        'Django-SupportTools<4.0',
        'Django-Safe-EmailBackend<2.0',
        'django_client_logger<3.0',
        'UW-HX-Toolkit==2.4.1',
        'django-blti<3.0',
        'yajl',
        'bleach',
        'pyyaml',
        'ua-parser',
        'user-agents',
        'django-user-agents',
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
