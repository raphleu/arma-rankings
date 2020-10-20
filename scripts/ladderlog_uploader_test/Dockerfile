FROM python:2.7-buster

RUN apt-get update
RUN apt-get install -y sqlite3 vim

WORKDIR /home/log_upload_service

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY armarankings-8ca076bc5be2.json armarankings-8ca076bc5be2.json
ENV GOOGLE_APPLICATION_CREDENTIALS=/home/log_upload_service/armarankings-8ca076bc5be2.json

COPY upload_ladderlog.py upload_ladderlog.py
COPY ladderlog.txt ladderlog.txt
ENTRYPOINT [ "/bin/bash" ]