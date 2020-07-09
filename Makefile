build-dev:
	docker-compose build --no-cache

run-dev:
	docker-compose up -d

create-db:
	docker-compose exec web python manage.py create_db

migrate:
	docker-compose exec web python manage.py db init

psql:
	docker-compose exec db psql --username=postgres --dbname=postgres

down-dev:
	docker-compose down

build-prod:
	docker-compose -f docker-compose.prod.yml build --no-cache

run-prod:
	docker-compose -f docker-compose.prod.yml up -d

down-prod:
	docker-compose -f docker-compose.prod.yml down