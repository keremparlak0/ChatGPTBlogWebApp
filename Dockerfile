FROM python:3.9.13-slim-buster

ENV PYTHONUNBUFFERED=1
WORKDIR /CHATGPT
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

