FROM python:2.7-buster

RUN useradd -ms /bin/bash ranking_app

WORKDIR /home/ranking_app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn==0.17.0
COPY app app
COPY raw_data raw_data

# set the owning group for raw_data to ranking_app so that we can update data from the running app 
RUN chown -R root:ranking_app raw_data
# allow owning groups to read and write stuff in raw_data 
RUN chmod -R g+rw raw_data

COPY scripts scripts
COPY tron-ranking.py config.py ./

ENV FLASK_APP tron-ranking.py

ARG RATING_TYPE
ENV RATING_TYPE=$RATING_TYPE

RUN flask db init
RUN flask db migrate -m "trueskill rankings"
RUN flask db upgrade

# set the owning group for database to ranking_app so that we can update data from the running app 
RUN chown root:ranking_app app.db
# allow owning groups to read and write stuff in database 
RUN chmod g+rw app.db

WORKDIR /home/ranking_app/scripts

RUN rm -f armarankings*

WORKDIR /home/ranking_app

USER ranking_app
EXPOSE 5000

ENTRYPOINT python /home/ranking_app/scripts/import_data.py && python /home/ranking_app/scripts/rank_trueskill.py && exec gunicorn --bind :5000 --access-logfile - --error-logfile - tron-ranking:app
