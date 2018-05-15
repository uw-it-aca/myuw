FROM python:2.7
ENV PYTHONUNBUFFERED 1
WORKDIR /app
ADD . /app/
ENV DB sqlite3
RUN pip install mysqlclient
RUN pip install -r requirements.txt
RUN django-admin.py startproject project .
ADD travis-ci /app/project/
