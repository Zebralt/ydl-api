FROM python:3.7

WORKDIR /app

# So that this isn't run every single fuck**g time
ADD ./requirements.txt /app
RUN pip3 install -r requirements.txt

ADD . /app

EXPOSE 8080

# https://pgjones.gitlab.io/quart/deployment.html
CMD hypercorn -b :8080 main:app
