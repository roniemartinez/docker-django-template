FROM python:3.10-slim-buster
LABEL maintainer="ronmarti18@gmail.com"

RUN apt update && apt install -y build-essential gettext python3-dev
RUN pip install -U poetry pip setuptools

ENV PYTHONUNBUFFERED=1

RUN mkdir /code
WORKDIR /code
COPY . /code/

RUN poetry config virtualenvs.create false
RUN poetry install
