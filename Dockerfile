FROM python:2.7-buster

RUN adduser ranking_app

WORKDIR /home/ranking_app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn==0.17.0
COPY app app
COPY migrations migrations
COPY raw_data raw_data
COPY scripts scripts
COPY tron-ranking.py config.py ./

ENV FLASK_APP tron-ranking.py

ARG RATING_TYPE
ENV RATING_TYPE=$RATING_TYPE

RUN flask db upgrade
WORKDIR /home/ranking_app/scripts
RUN python import_data.py
RUN python rank_trueskill.py

RUN rm -f armarankings*

WORKDIR /home/ranking_app

USER ranking_app
EXPOSE 5000

ENTRYPOINT exec gunicorn --bind :5000 --access-logfile - --error-logfile - tron-ranking:app
