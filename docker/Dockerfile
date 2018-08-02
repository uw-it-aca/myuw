FROM ubuntu
WORKDIR /app/
ADD docker/web/start.sh /start.sh
RUN chmod +x /start.sh
RUN mkdir /app/logs
RUN apt-get -y update && \
    apt-get -y install apache2 && \
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
    python-dev \
    libapache2-mod-wsgi \
    libxml2-dev \
    libxmlsec1-dev \
    python-pip \
    libmysqlclient-dev

RUN pip install --upgrade pip
ENV PYTHONUNBUFFERED 1
ADD myuw/VERSION /app/myuw/
RUN pip install mysqlclient
ADD setup.py /app/
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD /docker/web/apache2.conf /tmp/apache2.conf
RUN rm -rf /etc/apache2/sites-available/ && mkdir /etc/apache2/sites-available/ && \
    rm -rf /etc/apache2/sites-enabled/ && mkdir /etc/apache2/sites-enabled/ && \
    rm /etc/apache2/apache2.conf && \
    cp /tmp/apache2.conf /etc/apache2/apache2.conf &&\
    mkdir /etc/apache2/logs
ADD . /app/
ENV DB sqlite3
RUN django-admin.py startproject project .
ADD docker /app/project/
CMD ["/start.sh"]
