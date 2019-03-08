FROM acait/django-container:python3
RUN apt-get update && apt-get install mysql-client -y
RUN mkdir /app/logs
ADD myuw/VERSION /app/myuw/
ADD setup.py /app/
ADD requirements.txt /app/
RUN . /app/bin/activate && pip install -r requirements.txt
ADD /docker/web/apache2.conf /tmp/apache2.conf
RUN rm -rf /etc/apache2/sites-available/ && \
    mkdir /etc/apache2/sites-available/ && \
    rm -rf /etc/apache2/sites-enabled/ && \
    mkdir /etc/apache2/sites-enabled/ && \
    rm /etc/apache2/apache2.conf && \
    cp /tmp/apache2.conf /etc/apache2/apache2.conf && \
    mkdir /etc/apache2/logs
ADD . /app/
ENV DB sqlite3
ADD docker /app/project/
ADD docker/web/start.sh /start.sh
RUN chmod +x /start.sh
RUN mkdir /static

RUN groupadd -r myuw -g 1000 && \
    useradd -u 1000 -rm -g myuw -d /home/myuw -s /bin/bash -c "container user" myuw &&\
    chown -R myuw:myuw /app &&\
    chown -R myuw:myuw /static &&\
    chown -R myuw:myuw /var &&\
    chown -R myuw:myuw /run &&\
    mkdir /var/lock/apache2 &&\
    chown -R myuw:myuw /var/lock/ &&\
    chown -R myuw:myuw /home/myuw
USER myuw

RUN . /app/bin/activate && pip install nodeenv && nodeenv -p &&\
    npm install -g npm &&\
    ./bin/npm install less -g &&\
    ./bin/npm install datejs -g &&\
    ./bin/npm install jquery -g &&\
    ./bin/npm install moment -g &&\
    ./bin/npm install moment-timezone -g &&\
    ./bin/npm install jsdom -g
RUN . /app/bin/activate && python manage.py collectstatic &&\
    python manage.py compress

CMD ["/start.sh" ]
