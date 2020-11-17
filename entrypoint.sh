#!/bin/bash
if [ "${FLASK_ENV}" = "cloud" ]; then
    python /home/ranking_app/scripts/import_data.py
    python /home/ranking_app/scripts/import_GCP_storage_data.py
    python /home/ranking_app/scripts/rank_trueskill.py
    exec gunicorn --bind :5000 --access-logfile - --error-logfile - tron-ranking:app
else
    python /home/ranking_app/scripts/rank_trueskill.py
    exec gunicorn --bind :5000 --access-logfile - --error-logfile - tron-ranking:app
fi
