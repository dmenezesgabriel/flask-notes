# Development
build-dev:
	docker-compose build --no-cache web

run-dev:
	docker-compose up web

create-db:
	docker-compose exec web python manage.py create_db

seed-db:
	docker-compose exec web python manage.py seed_db

migrate:
	docker-compose exec web python manage.py db init

psql:
	docker-compose exec db psql --username=postgres --dbname=postgres

down-dev:
	docker-compose down

dev-bash:
	docker-compose exec web /bin/sh

# Test
build-test:
	docker-compose build --no-cache test

run-test:
	docker-compose up test

# Production
build-prod:
	docker-compose -f docker-compose.prod.yml build --no-cache

run-prod:
	docker-compose -f docker-compose.prod.yml up -d

create-db-prod:
	docker-compose -f docker-compose.prod.yml exec web python manage.py create_db

email-test-server:
	python -m smtpd -n -c DebuggingServer localhost:8025