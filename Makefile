.PHONY: install
install:
	pip3 install -U pip setuptools poetry
	poetry install

.PHONY: format
format:
	poetry run autoflake --remove-all-unused-imports --in-place -r --exclude __init__.py .
	poetry run isort .
	poetry run black .

.PHONY: lint
lint:
	poetry run autoflake --remove-all-unused-imports --in-place -r --exclude __init__.py --check .
	poetry run isort --check-only .
	poetry run black --check .
	poetry run pflake8 .
	poetry run mypy .

.PHONY: test
test:
	docker-compose run --rm web bash -c "pytest"

.PHONY: build
build:
	docker-compose build

.PHONY: start
start:
	docker-compose up

.PHONY: superuser
superuser:
	docker-compose run --rm web bash -c "python manage.py createsuperuser"

.PHONY: migrations
migrations:
	docker-compose run --rm web bash -c "python manage.py makemigrations"

.PHONY: migrate
migrate:
	docker-compose run --rm web bash -c "python manage.py migrate"

.PHONY: messages
messages:
	docker-compose run --rm web bash -c "python manage.py makemessages -a --no-obsolete -v 3 --ignore 'htmlcov/*' --ignore '*migrations*'"

.PHONY: compilemessages
compilemessages:
	docker-compose run --rm web bash -c "python manage.py compilemessages"

.PHONY: dumpdata
dumpdata:
	docker-compose run --rm web bash -c "python manage.py dumpdata --format json --indent 2 -o backups/dump.json -v 3"

.PHONY: loaddata
loaddata:
	docker-compose run --rm web bash -c "python manage.py loaddata -e auth.permission -v 3"
