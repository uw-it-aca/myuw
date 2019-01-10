FROM acait/django-container:python3
RUN apt-get install mysql-client -y
RUN mkdir /app/logs
ADD myuw/VERSION /app/myuw/
ADD setup.py /app/
ADD requirements.txt /app/
RUN . /app/bin/activate && pip install -r requirements.txt
ADD /docker/web/apache2.conf /tmp/apache2.conf
RUN rm -rf /etc/apache2/sites-available/ && mkdir /etc/apache2/sites-available/ && \
    rm -rf /etc/apache2/sites-enabled/ && mkdir /etc/apache2/sites-enabled/ && \
    rm /etc/apache2/apache2.conf && \
    cp /tmp/apache2.conf /etc/apache2/apache2.conf &&\
    mkdir /etc/apache2/logs
ADD . /app/
ENV DB sqlite3
ADD docker /app/project/
ADD docker/web/start.sh /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh" ]
