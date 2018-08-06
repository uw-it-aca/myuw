#!/bin/bash
# Remove any existing httpd data
rm -rf /run/httpd/* /tmp/httpd*


# Check if we're the leader using ElasticBeanstalk's methods
if [ -f /tmp/is_leader ]; then
    python manage.py migrate
fi

pip install -r requirements.txt
pip uninstall -y uw-restclients-core
pip install -e git+https://github.com/uw-it-aca/uw-restclients-core@bug/memcached-mock-error#egg=uw-restclients-core

rm -rf /static/
python manage.py collectstatic

# Start Apache server in foreground
exec /usr/sbin/apachectl -DFOREGROUND
