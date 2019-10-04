

tag=ydlapi-front
hostport=8085
network=host
library=$(shell pwd)/d
view=true
ip=$(shell ip a | grep wlo1 | grep -o 'inet \([0-9.]\+\)' | cut -d' ' -f2)


all: kill rm build run p

build:
	docker build . -t $(tag) --no-cache

run:
	docker run -d -p $(hostport):80 $(tag)
	
	# (($(view))) && sleep 1 && xdg-open http://localhost:$(hostport)

	if [ "$(view)" = true ]; then \
		sleep 1 && xdg-open http://$(ip):$(hostport) \
	;fi

kill:
	docker ps | grep $(tag) | cut -d' ' -f1 | xargs -r docker kill

rm:
	docker ps -a | grep $(tag) | cut -d' ' -f1 | xargs -r docker rm

log:
	docker ps -a | grep $(tag) | head -n 1 | cut -d' ' -f1 | xargs -r docker logs

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