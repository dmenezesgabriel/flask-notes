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