run_backend:
	fastapi dev ./backend/src/main.py

compose:
	docker-compose up

load_elastic:
	python ./backend/src/database/load_meilisearch.py
load_qdrant:
	python ./backend/src/database/load_qdrant.py

build-image:
	docker build -t mori:latest .

swarm: build-image
	docker swarm init
	@echo swarm has been initiated
	docker stack deploy -c docker-compose.yml mori-app
	@echo swarm has been run successfully

stop-swarm:
	docker swarm leave --force
