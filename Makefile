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

.PHONY: type
type:
	poetry run mypy --ignore-missing-imports .

.PHONY: test
test:
	DJANGO_SECRET_KEY=test POSTGRES_DB=test POSTGRES_USER=test poetry run coverage run --source="sample" manage.py test -v 2
	poetry run coverage html --omit="*/test*,*/apps.py"

.PHONY: build
build:
	docker-compose build

.PHONY: up
up:
	docker-compose up
