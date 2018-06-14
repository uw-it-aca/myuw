FROM python:2.7
WORKDIR /app/
ENV PYTHONUNBUFFERED 1
ADD myuw/VERSION /app/myuw/
RUN pip install mysqlclient
ADD setup.py /app/
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /app/
ENV DB sqlite3
RUN django-admin.py startproject project .
ADD docker /app/project/
