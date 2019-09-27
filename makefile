
tag=ydlapi
hostport=8080
network=host
library=$(shell pwd)/d

all: kill build run p

build:
	docker build . -t $(tag)

run:
	docker run -d --network=$(network) --mount type=bind,source=$(library),target=/music $(tag)
	sleep 1 && xdg-open http://localhost:$(hostport)

kill:
	docker ps | grep ydlapi | cut -d' ' -f1 | xargs -r docker kill

start:
	hypercorn --debug -b :8080 main:app

k: kill
b: build
r: run
p:
	docker ps
l:
	docker ps -a | grep ydlapi | head -n 1 | cut -d' ' -f1 | xargs -r docker logs