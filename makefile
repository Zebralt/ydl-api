

all: k
	docker-compose up -d

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