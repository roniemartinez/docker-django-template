FROM python:3.8.7-slim-buster
LABEL maintainer="ronmarti18@gmail.com"

RUN apt update && apt install -y build-essential gettext python3-dev
RUN pip install poetry

ENV PYTHONUNBUFFERED=1

RUN mkdir /code
WORKDIR /code
COPY . /code/

RUN poetry install --no-dev
