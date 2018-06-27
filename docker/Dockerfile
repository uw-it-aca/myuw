FROM centos
WORKDIR /app/
ADD web/start.sh /start.sh
RUN chmod +x /start.sh
RUN mkdir /app/logs
RUN yum -y --setopt=tsflags=nodocs update && \
    yum -y --setopt=tsflags=nodocs install httpd && \
    yum clean all

# Install yum dependencies
RUN yum -y update && \
    yum groupinstall -y development && \
    yum install -y \
    bzip2-devel \
    git \
    hostname \
    openssl \
    openssl-devel \
    sqlite-devel \
    sudo \
    tar \
    wget \
    zlib-dev \
    python-devel \
    mod_wsgi

# Install setuptools + pip
RUN cd /tmp && \
    curl https://bootstrap.pypa.io/get-pip.py | python - && \
    pip install setuptools
ENV PYTHONUNBUFFERED 1
ADD ../myuw/VERSION /app/myuw/
RUN yum install -y mysql-devel
RUN pip install mysqlclient
ADD ../setup.py /app/
ADD ../requirements.txt /app/
RUN pip install -r requirements.txt
ADD web/httpd.conf /tmp/httpd.conf
RUN cat /tmp/httpd.conf > /etc/httpd/conf/httpd.conf
ADD .. /app/
ENV DB sqlite3
RUN django-admin.py startproject project .
ADD docker /app/project/
CMD ["/start.sh"]
