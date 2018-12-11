#!/bin/bash
# Remove any existing httpd data
rm -rf /run/httpd/* /tmp/httpd*


# Check if we're the leader using ElasticBeanstalk's methods
python3 manage.py migrate

pip3 install -r requirements.txt

rm -rf /static/
python3 manage.py collectstatic

# Start Apache server in foreground
exec /usr/sbin/apachectl -DFOREGROUND
