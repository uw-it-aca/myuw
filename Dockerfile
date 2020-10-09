FROM acait/django-container:1.1.7 as app-container

USER root
RUN apt-get update && apt-get install mysql-client libmysqlclient-dev -y
USER acait

ADD --chown=acait:acait myuw/VERSION /app/myuw/
ADD --chown=acait:acait setup.py /app/
ADD --chown=acait:acait requirements.txt /app/
RUN . /app/bin/activate && pip install -r requirements.txt

RUN . /app/bin/activate && pip install mysqlclient

ADD --chown=acait:acait . /app/
ADD --chown=acait:acait docker/ project/

RUN . /app/bin/activate &&\
    pip install nodeenv &&\
    nodeenv -p &&\
    npm install -g npm &&\
    ./bin/npm install less -g

RUN . /app/bin/activate && python manage.py collectstatic --noinput &&\
    python manage.py compress -f

RUN . /app/bin/activate && python manage.py test
FROM acait/django-test-container:1.1.7 as app-test-container

COPY --from=app-container /app/ /app/
COPY --from=app-container /static/ /static/
