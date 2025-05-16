FROM python:3.10.2-slim

WORKDIR /app
COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && pipenv install --system

COPY . .