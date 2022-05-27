FROM gcr.io/uwit-mci-axdd/django-container:1.3.8 as app-prewebpack-container

USER root
RUN apt-get update && apt-get install mysql-client libmysqlclient-dev -y
USER acait

ADD --chown=acait:acait myuw/VERSION /app/myuw/
ADD --chown=acait:acait setup.py /app/
ADD --chown=acait:acait requirements.txt /app/

RUN . /app/bin/activate && pip install -r requirements.txt

RUN . /app/bin/activate && pip install mysqlclient

# myuw does NOT have these scripts
#ADD --chown=acait:acait docker/app_start.sh /scripts
#RUN chmod u+x /scripts/app_start.sh

FROM node:16.3-stretch AS node-bundler

ADD ./package.json /app/
WORKDIR /app/
ENV NODE_ENV=production
RUN npm install .

ADD . /app/

ARG VUE_DEVTOOLS
ENV VUE_DEVTOOLS=$VUE_DEVTOOLS
RUN npx webpack --mode=production

FROM app-prewebpack-container as app-container

ADD --chown=acait:acait . /app/
ADD --chown=acait:acait docker/ project/
ADD --chown=acait:acait docker/app_start.sh /scripts
RUN chmod u+x /scripts/app_start.sh

COPY --chown=acait:acait --from=node-bundler /app/myuw/static /app/myuw/static

RUN . /app/bin/activate && python manage.py collectstatic --noinput

FROM gcr.io/uwit-mci-axdd/django-test-container:1.3.8 as app-test-container

ENV NODE_PATH=/app/lib/node_modules
COPY --from=app-container /app/ /app/
COPY --from=app-container /static/ /static/

FROM node-bundler AS node-test-container

ENV NODE_ENV=development
RUN npm install
