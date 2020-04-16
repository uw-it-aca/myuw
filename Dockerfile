FROM acait/django-container:1.0.22 as myuw

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

FROM myuw as myuw-test
USER root
RUN apt-get install -y nodejs npm rubygems &&\
    pip install pycodestyle coverage &&\
    gem install coveralls-lcov &&\
    nodeenv -p &&\
    npm install tslib -g &&\
    npm install datejs -g &&\
    npm install jquery -g &&\
    npm install moment -g &&\
    npm install moment-timezone -g &&\
    npm install jsdom@15.2.1 -g &&\
    npm install jshint -g &&\
    npm install mocha -g &&\
    npm install nyc -g &&\
    npm install sinon -g &&\
    npm install coveralls -g
