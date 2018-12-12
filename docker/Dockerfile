FROM ubuntu
WORKDIR /app/
ADD docker/web/start.sh /start.sh
RUN chmod +x /start.sh
RUN mkdir /app/logs
RUN apt-get -y update && \
    apt-get -y install apache2 apache2-mpm-worker apache2-threaded-dev && \
    apt-get clean all

# Install system dependencies
RUN apt-get -y update && \
    apt-get install -y \
    git \
    hostname \
    openssl \
    sqlite3 \
    sudo \
    tar \
    curl \
    wget \
    python-setuptools \
    build-essential\
    python3.6-dev \
    libxml2-dev \
    libxmlsec1-dev \
    python-pip \
    libmysqlclient-dev

RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
RUN pip3 install --upgrade pip
RUN pip3 install mod_wsgi
RUN pip3 install boto3 watchtower
ENV PYTHONUNBUFFERED 1
ADD myuw/VERSION /app/myuw/
RUN pip install mysqlclient
ADD setup.py /app/
ADD requirements.txt /app/
RUN pip3 install -r requirements.txt
ADD /docker/web/apache2.conf /tmp/apache2.conf
RUN rm -rf /etc/apache2/sites-available/ && mkdir /etc/apache2/sites-available/ && \
    rm -rf /etc/apache2/sites-enabled/ && mkdir /etc/apache2/sites-enabled/ && \
    rm /etc/apache2/apache2.conf && \
    cp /tmp/apache2.conf /etc/apache2/apache2.conf &&\
    mkdir /etc/apache2/logs
ADD . /app/
ENV DB sqlite3
RUN rm -rf project/ && rm -f manage.py && django-admin.py startproject project .
ADD docker /app/project/
CMD ["/start.sh"]
