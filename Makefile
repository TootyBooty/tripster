up:
	docker compose -f docker-compose.yml up -d

down:
	docker compose -f docker-compose.yml down

reload:
	docker compose -f docker-compose.yml up --build --detach
