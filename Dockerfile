FROM python:3.6

RUN pip3 install -r requirements.txt

ADD . /app
WORKDIR /app

# MOUNT host machine
# NETWORK ?

EXPOSE 8080

CMD gunicorn -b :8080 main:app
