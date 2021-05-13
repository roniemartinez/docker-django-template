.PHONY: install
install:
	pip3 install -U poetry
	poetry install

.PHONY: style
style:
	poetry run autoflake --remove-all-unused-imports --in-place -r .
	poetry run isort --atomic .
	poetry run black .
	poetry run flake8 .

.PHONY: format
format: style

.PHONY: type
type:
	poetry run mypy .

.PHONY: test
test:
	docker-compose run --rm web bash -c "pytest"

.PHONY: build
build:
	docker-compose build

.PHONY: up
up:
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
	docker-compose run --rm web bash -c "python manage.py makemessages -a --no-obsolete"

.PHONY: compilemessages
compilemessages:
	docker-compose run --rm web bash -c "python manage.py compilemessages"

.PHONY: cachetable
cachetable:
	docker-compose run --rm web bash -c "python manage.py createcachetable"
