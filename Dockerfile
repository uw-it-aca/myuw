FROM acait/django-container:1.0

USER root
RUN apt-get update && apt-get install mysql-client -y
USER acait

ADD --chown=acait:acait myuw/VERSION /app/myuw/
ADD --chown=acait:acait setup.py /app/
ADD --chown=acait:acait requirements.txt /app/
RUN . /app/bin/activate && pip install -r requirements.txt
ADD . /app/

ADD docker /app/project/


RUN . /app/bin/activate && pip install nodeenv && nodeenv -p &&\
    npm install -g npm &&\
    ./bin/npm install tslib -g &&\
    ./bin/npm install less -g &&\
    ./bin/npm install datejs -g &&\
    ./bin/npm install jquery -g &&\
    ./bin/npm install moment -g &&\
    ./bin/npm install moment-timezone -g &&\
    ./bin/npm install jsdom -g
RUN . /app/bin/activate && python manage.py collectstatic &&\
    python manage.py compress

