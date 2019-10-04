

all: k
	docker-compose up -d
	xdg-open http://0.0.0.0:8085

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