FROM python:3.9-alpine

RUN apk add --no-cache \
    gcc g++ libc-dev

RUN pip install --upgrade \
    pip setuptools

WORKDIR /usr/src/app