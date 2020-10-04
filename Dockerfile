FROM acait/django-container:1.1.3 as pre-container

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
RUN npx webpack --production

FROM pre-container as app-container

COPY --chown=acait:acait --from=node-bundler /static /static

RUN . /app/bin/activate && python manage.py collectstatic --noinput

FROM acait/django-test-container:1.1.3 as app-test-container

ENV NODE_PATH=/app/lib/node_modules
COPY --from=app-container /app/ /app/
COPY --from=app-container /static/ /static/
