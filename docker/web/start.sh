#!/bin/bash
# Remove any existing httpd data
rm -rf /run/httpd/* /tmp/httpd*

pip install -r requirements.txt
rm -rf /static/
python manage.py collectstatic
# Start Apache server in foreground
exec /usr/sbin/apachectl -DFOREGROUND
