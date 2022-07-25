FROM python:3.10.5
ENV PYTHONUNBUFFERED 1

WORKDIR /app
ADD    requirements.txt   /app/
RUN    apt-get update -y
RUN    pip install --upgrade pip && pip install -r requirements.txt
