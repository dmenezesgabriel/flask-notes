run-dev:
	docker-compose up -d

create-db:
	docker-compose exec web python manage.py create_db

psql:
	docker-compose exec db psql --username=postgres --dbname=postgres