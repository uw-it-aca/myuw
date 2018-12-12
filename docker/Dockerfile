FROM ubuntu
WORKDIR /app/
ADD docker/web/start.sh /start.sh
RUN chmod +x /start.sh
RUN mkdir /app/logs
RUN apt-get -y update && \
    apt-get -y install apache2 apache2-dev && \
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
    python3-venv \
    libxml2-dev \
    libxmlsec1-dev \
    python-pip \
    libmysqlclient-dev

RUN python3 -m venv /app/
RUN . /app/bin/activate && wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py && pip3 install --upgrade pip && pip install mod_wsgi && pip install boto3 watchtower && pip install mysqlclient
ENV PYTHONUNBUFFERED 1
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
RUN . /app/bin/activate && rm -rf project/ && rm -f manage.py && django-admin.py startproject project .
ADD docker /app/project/
CMD ["/start.sh" ]
