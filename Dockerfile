FROM gcr.io/uwit-mci-axdd/django-container:1.3.3 as pre-container
# Has to be pre-container

USER root
RUN apt-get update && apt-get install mysql-client libmysqlclient-dev -y
USER acait

ADD --chown=acait:acait myuw/VERSION /app/myuw/
ADD --chown=acait:acait setup.py /app/
ADD --chown=acait:acait requirements.txt /app/
RUN . /app/bin/activate && pip install -r requirements.txt
RUN . /app/bin/activate && pip install mysqlclient

FROM node:16.3-stretch-slim AS node-bundler

ADD ./package.json /app/
WORKDIR /app/
ENV NODE_ENV=production
RUN npm install

ADD . /app/
ARG VUE_DEVTOOLS
ENV VUE_DEVTOOLS=$VUE_DEVTOOLS
RUN ./node_modules/.bin/webpack

FROM pre-container as app-container
COPY --chown=acait:acait --from=node-bundler /static /static

ADD --chown=acait:acait . /app/
ADD --chown=acait:acait docker/ project/

RUN . /app/bin/activate && python manage.py collectstatic --noinput

FROM node-bundler AS node-test-container

ENV NODE_ENV=development
RUN npm install

FROM gcr.io/uwit-mci-axdd/django-test-container:1.3.3 as app-test-container

ENV NODE_PATH=/app/lib/node_modules
COPY --from=app-container /app/ /app/
COPY --from=app-container /static/ /static/
