FROM python:2.7
WORKDIR /app/
ENV PYTHONUNBUFFERED 1
ADD myuw/VERSION /app/myuw/
RUN apt-get update && apt-get install -qq python-dev libxml2-dev libxmlsec1-dev
RUN pip install mysqlclient
ADD setup.py /app/
ADD requirements.txt /app/
RUN pip install -r requirements.txt
RUN pip install boto3
ADD . /app/
ENV DB sqlite3
RUN django-admin.py startproject project .
ADD docker /app/project/
ENV REMOTE_USER javerage
CMD ["python", "manage.py", "runserver", "0:8000"]
