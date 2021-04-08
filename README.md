# Docker+Django Template

Template repository for a Docker+Django project

## Build and run

Note: update the environment variables in `env` folder before running the following commands:

```shell
docker-compose build
docker-compose up
```

## Scaling

To scale up, add --scale web=N parameter. For example:

```shell
docker-compose up --scale web=3
```

## Add translations

```shell
poetry run python manage.py makemessages -l <language_code>
# edit and translate locale/<language_code>/LC_MESSAGES/django.po
```

## Development

Use the `Makefile` included for running different development tasks:

1. `make install` - installs the packages needed for development.
2. `make style` or `make format` - runs `autoflake`, `isort`, `black` and `flake8` for fixing coding style. 
3. `make type` - type checking using `mypy`.
4. `make test` - run unit tests.
5. `make migrations` - generate migration scripts, if applicable.
6. `make migrate` - run migrations, if applicable.
7. `make superuser` - create superuser.

## Author

[Ronie Martinez](mailto:ronmarti18@gmail.com)
