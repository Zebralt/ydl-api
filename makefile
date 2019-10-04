

all: rm k build run

build:
	docker-compose build
	@echo

run:
	docker-compose up -d
	xdg-open http://0.0.0.0:8085

rm:
	cd front && make rm
	cd back && make rm

k:
	@docker-compose down || echo

ka: k
	cd front && make k
	cd back && make k

f:
	cd front && make

b:
	cd back && make

p:
	docker ps