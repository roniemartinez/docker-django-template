#!/bin/bash

if [[ "${DEBUG}" == "true" ]]; then
  poetry run python manage.py runserver 0.0.0.0:8000
else
  poetry run daphne -b 0.0.0.0 project.asgi:application
fi
