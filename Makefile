# Development
build-dev:
	docker-compose build --no-cache

run-dev:
	docker-compose up

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

# Translation
# 1.
extract-pot:
# The pybabel extract command reads the configuration file given in the -F option,
# by default, pybabel will look for _() as a text marker, but I have also used
# the lazy version, which I imported as _l(), so I need to tell the tool
# to look for those too with the -k _l. The -o option provides the name of
# the output file.
	docker-compose run --rm web pybabel extract -F babel.cfg -k _l -o messages.pot .

# 2.
catalog-lang-pt:
	docker-compose run --rm web pybabel init -i messages.pot -d src/translations -l pt

# 3.
compile-translations:
# This operation adds a messages.mo file next to messages.po in each language
# repository. The .mo file is the file that Flask-Babel will use to load
# translations for the application.
	docker-compose run --rm web pybabel compile -d src/translations

update-translations:
	docker-compose run --rm web pybabel update -i messages.pot -d src/translations

# Production
build-prod:
	docker-compose -f docker-compose.prod.yml build --no-cache

run-prod:
	docker-compose -f docker-compose.prod.yml up -d

create-db-prod:
	docker-compose -f docker-compose.prod.yml exec web python manage.py create_db

email-test-server:
	python -m smtpd -n -c DebuggingServer localhost:8025