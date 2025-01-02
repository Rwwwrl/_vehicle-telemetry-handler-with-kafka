up:
	docker-compose up -d

down:
	docker-compose down

restart:
	$(MAKE) down
	$(MAKE) up
