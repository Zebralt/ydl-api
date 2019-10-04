FROM nginx:alpine

WORKDIR /usr/share/nginx/html/

COPY ./view/* /usr/share/nginx/html/
COPY styles /usr/share/nginx/html/styles
COPY scripts /usr/share/nginx/html/scripts

# CMD ls