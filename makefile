
tag=ydlapi
hostport=8080
network=host

all: kill build run p

build:
	docker build . -t $(tag)

run:
	docker run -d --network=$(network) $(tag)
	docker ps
	sleep 1 && xdg-open http://localhost:$(hostport)

kill:
	docker ps | grep ydlapi | cut -d' ' -f1 | xargs docker kill

k: kill
b: build
r: run
p:
	docker ps

