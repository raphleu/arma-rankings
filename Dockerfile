FROM python:2.7-alpine

RUN adduser -D ranking_app

WORKDIR /home/ranking_app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app app
COPY migrations migrations
COPY raw_data raw_data
COPY scripts scripts
COPY tron-ranking.py config.py ./

ENV FLASK_APP tron-ranking.py

RUN flask db upgrade
WORKDIR /home/ranking_app/scripts
RUN python load_matches.py

WORKDIR /home/ranking_app

EXPOSE 5000

ENTRYPOINT flask run --host 0.0.0.0
