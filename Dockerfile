ARG DJANGO_CONTAINER_VERSION=3.0.2
FROM us-docker.pkg.dev/uwit-mci-axdd/containers/django-container:${DJANGO_CONTAINER_VERSION} AS app-prewebpack-container

USER root
RUN apt-get update && apt-get install --no-install-recommends -y postgresql-client libpq-dev && apt-get -y autoremove && apt-get clean && rm -rf /var/lib/apt/lists/*
USER acait

COPY --chown=acait:acait . /app/
COPY --chown=acait:acait docker/ /app/project/
COPY --chown=acait:acait docker/app_start.sh /scripts
RUN chmod u+x /scripts/app_start.sh && /app/bin/pip install -r requirements.txt psycopg2

# latest node + ubuntu
FROM node:24 AS node-base
FROM ubuntu:24.04 AS node-bundler
COPY --from=node-base / /

COPY ./package.json /app/
WORKDIR /app/
ENV NODE_ENV=production
RUN npm install .

COPY . /app/

ARG VUE_DEVTOOLS
ENV VUE_DEVTOOLS=$VUE_DEVTOOLS
RUN npx webpack --mode=production

FROM app-prewebpack-container AS app-container

COPY --chown=acait:acait --from=node-bundler /app/myuw/static /app/myuw/static
RUN /app/bin/python manage.py collectstatic --noinput

FROM us-docker.pkg.dev/uwit-mci-axdd/containers/django-test-container:${DJANGO_CONTAINER_VERSION} AS app-test-container

ENV NODE_PATH=/app/lib/node_modules
COPY --from=app-container /app/ /app/
COPY --from=app-container /static/ /static/

FROM node-bundler AS node-test-container

ENV NODE_ENV=development
RUN npm install
