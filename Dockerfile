FROM python:3-alpine
COPY . /poll
WORKDIR /poll
RUN pip install -r requirements.txt
RUN python manage.py migrate --noinput
RUN python manage.py createsuperuser
EXPOSE 3005