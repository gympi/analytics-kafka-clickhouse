FROM python:3.6

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /usr/src/app/

WORKDIR /usr/src/app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt