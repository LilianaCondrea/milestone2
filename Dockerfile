FROM python:3.9-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /apps

# Installing python dependencies
COPY . /apps
RUN python -m pip install --upgrade pip
RUN python -m pip install psycopg2
RUN python -m pip install -r requirements.txt

# Exposing Ports
EXPOSE 5432
EXPOSE 8080


