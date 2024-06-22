run_backend:
	fastapi dev ./backend/src/main.py

compose:
	docker-compose up

load_elastic:
	python ./backend/load_elasticsearch.py

load_qdrant:
	python ./backend/load_qdrant.py

build-image:
	docker build -t mori:latest .

swarm: build-image
	docker swarm init
	@echo swarm has been initiated
	docker stack deploy -c docker-compose.yml mori-app
	@echo swarm has been run successfully

stop-swarm:
	docker swarm leave --force