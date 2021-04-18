# Docker+Django Template

Template repository for a Docker+Django project

## What is in this template
- Scalable Django web app with login/registration and initial Bootstrap 4 template
- Nginx for load balancing traffic to the Django web apps when scaled
- PostgreSQL database
- Optional dockerized cron

## Demo

You can check this template in action using the URL [https://ddt.ron.sh/](https://ddt.ron.sh/)

## Creating a project from this Docker+Django Template



## Installation on a DigitalOcean Droplet and nginx (Optional)

If you don't have a DigitalOcean account yet, create one using my referral [link](https://m.do.co/c/5b9c0bd05e4e).

1. Create a Domain and add an `A record` pointing to your Droplet.
2. Inside your Droplet, create an SSL certificate:

```shell
certbot --nginx -d <domain>
```

3. Edit the nginx configuration (usually /etc/nginx/sites-available/default) and update the `location /` block just below the domain created by certbot (look for `server_name <domain>; # managed by Certbot`):
   
```
	location / {
            proxy_pass http://127.0.0.1:8081$request_uri;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_redirect off;
	}
```

4. Clone your project that was created using Docker+Django Template or you can create a non-git package (up to you).
5. Reload nginx:

```shell
service nginx reload
```

## Build and run

Note: update the environment variables in `env` folder before running the following commands:

```shell
cd <project-folder>
docker-compose build
docker-compose up  # or "docker-compose up -d" to run in detached mode
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
10. `make cachetable` - create cachetable.

## Author

[Ronie Martinez](mailto:ronmarti18@gmail.com)
