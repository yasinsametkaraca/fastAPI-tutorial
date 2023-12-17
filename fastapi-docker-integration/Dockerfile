FROM python:3.8.10-slim

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
