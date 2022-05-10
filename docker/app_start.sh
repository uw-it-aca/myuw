if [ "$ENV"  = "localdev" ]
then

  python manage.py migrate
  python manage.py loaddata persistent_messages.json

fi
