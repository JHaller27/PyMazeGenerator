FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
MAINTAINER James Haller <jameshaller27@gmail.com>

RUN mkdir -p /app
COPY . /app
WORKDIR /app
