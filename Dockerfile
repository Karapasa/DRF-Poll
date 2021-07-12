FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install -y python3-dev build-essential python3-pip
RUN pip3 install --upgrade setuptools

COPY . /poll
WORKDIR /poll
RUN pip3 install --upgrade pip -r requirements.txt
RUN python3 manage.py migrate --run-syncdb
RUN python3 manage.py collectstatic
EXPOSE 3005
