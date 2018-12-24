FROM continuumio/miniconda:latest

RUN apt-get update && apt-get install -y gcc

RUN mkdir /opt/movie5
WORKDIR /opt/movie5

ADD . /opt/movie5

RUN pip install -r requirements.txt

CMD gunicorn --bind 0.0.0.0:$PORT wsgi:app
