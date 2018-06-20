#!/bin/bash
# Remove any existing httpd data
rm -rf /run/httpd/* /tmp/httpd*

pip install -r requirements.txt
sleep 5
python manage.py migrate
rm -rf /static/
python manage.py collectstatic
# Start Apache server in foreground
REMOTE_USER=javerage exec /usr/sbin/apachectl -DFOREGROUND
