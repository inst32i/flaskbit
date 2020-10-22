FROM python:2.7
MAINTAINER kenybens "kenybens@gmail.com"
COPY requirements.txt /usr/www/app/
WORKDIR /usr/www/app

RUN pip install -r requirements.txt
CMD python flaskunit.py 0.0.0.0:5000

EXPOSE 5000 5000