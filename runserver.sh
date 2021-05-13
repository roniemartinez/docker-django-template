#!/bin/bash

if [[ "${DEBUG}" == "true" ]]; then
  python manage.py runserver 0.0.0.0:8000
else
  daphne -b 0.0.0.0 project.asgi:application
fi
