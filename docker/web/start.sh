#!/bin/bash
# Remove any existing httpd data
rm -rf /run/httpd/* /tmp/httpd*

source "/app/bin/activate"
export DATABASE_NAME=`echo $BRANCH | sed 's/-/_/g' `

if [ "$DB" = "mysql" ] && [ "$ENV" = "dev" ]
then
  mysql -u $DATABASE_USERNAME -p$DATABASE_PASSWORD -h $DATABASE_HOSTNAME --execute="create database `echo $DATABASE_NAME | sed 's/-/_/g' ` "
fi

python3 manage.py migrate

pip3 install -r requirements.txt

rm -rf /static/
python3 manage.py collectstatic

# Start Apache server in foreground
exec /usr/sbin/apachectl -DFOREGROUND
