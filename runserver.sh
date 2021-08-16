#!/bin/bash

if [[ "${DEBUG}" == "true" ]]; then
  python manage.py runserver 0.0.0.0:8081
else
  daphne -b 0.0.0.0 -p 8081 project.asgi:application
fi
