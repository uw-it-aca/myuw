FROM python:2.7
ENV PYTHONUNBUFFERED 1
WORKDIR /app
ADD . /app/
RUN pip install -r requirements.txt
ENV DB sqlite3
RUN django-admin.py startproject project .
ADD travis-ci /app/project/
ENV REMOTE_USER javerage
RUN python manage.py migrate