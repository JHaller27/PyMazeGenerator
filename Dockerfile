FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
MAINTAINER James Haller <jameshaller27@gmail.com>

RUN mkdir -p /app
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
