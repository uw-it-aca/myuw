FROM acait/django-container:1.1.7 as pre-container

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

FROM node:14.6.0-stretch AS node-bundler

ADD ./package.json /app/
WORKDIR /app/
RUN npm install .

ADD . /app/
RUN npx webpack

FROM pre-container as app-container

COPY --chown=acait:acait --from=node-bundler /static /static

RUN . /app/bin/activate && python manage.py collectstatic --noinput