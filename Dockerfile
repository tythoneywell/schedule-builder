#syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /flask_app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY flask_app/. .

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]

