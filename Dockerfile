ARG DJANGO_CONTAINER_VERSION=1.4.2
FROM us-docker.pkg.dev/uwit-mci-axdd/containers/django-container:${DJANGO_CONTAINER_VERSION} as app-container

USER root
RUN apt-get update && apt-get install mysql-client libmysqlclient-dev -y
USER acait

ADD --chown=acait:acait . /app/
ADD --chown=acait:acait docker/ /app/project/
ADD --chown=acait:acait docker/app_start.sh /scripts
RUN chmod u+x /scripts/app_start.sh

RUN /app/bin/pip install -r requirements.txt
RUN /app/bin/pip install mysqlclient

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

COPY --chown=acait:acait --from=node-bundler /app/myuw/static /app/myuw/static
RUN /app/bin/python manage.py collectstatic --noinput

FROM us-docker.pkg.dev/uwit-mci-axdd/containers/django-test-container:${DJANGO_CONTAINER_VERSION} as app-test-container

ENV NODE_PATH=/app/lib/node_modules
COPY --from=app-container /app/ /app/
COPY --from=app-container /static/ /static/

FROM node-bundler AS node-test-container

ENV NODE_ENV=development
RUN npm install
