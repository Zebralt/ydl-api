
tag=ydlapi
hostport=8080
network=host
library=$(shell pwd)/d
view=true

all: kill build run p

build:
	docker build . -t $(tag)

run:
	docker run -d --network=$(network) --mount type=bind,source=$(library),target=/music $(tag)
	
	# (($(view))) && sleep 1 && xdg-open http://localhost:$(hostport)

	if [ "$(view)" = true ]; then \
		sleep 1 && xdg-open http://localhost:$(hostport) \
	;fi

kill:
	docker ps | grep ydlapi | cut -d' ' -f1 | xargs -r docker kill

start:
	hypercorn --debug -b :8080 main:app

log:
	docker ps -a | grep ydlapi | head -n 1 | cut -d' ' -f1 | xargs -r docker logs

ps:
	docker ps

watch:
	watch make l

k: kill
b: build
r: run
p: ps
l: log
w: watch