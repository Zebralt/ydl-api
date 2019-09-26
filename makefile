
tag=ydlapi
hostport=8080
network=host
library=$(shell pwd)/d

all: kill build run p

build:
	docker build . -t $(tag)

run:
	echo $(library)
	docker run -d --network=$(network) --mount type=bind,source=$(library),target=/music $(tag)
	sleep 1 && xdg-open http://localhost:$(hostport)

kill:
	docker ps | grep ydlapi | cut -d' ' -f1 | xargs -r docker kill

k: kill
b: build
r: run
p:
	docker ps

