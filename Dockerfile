FROM python:3.7

ADD . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

# MOUNT host machine
# NETWORK ?

EXPOSE 8080

# https://pgjones.gitlab.io/quart/deployment.html
CMD hypercorn -b :8080 main:app
