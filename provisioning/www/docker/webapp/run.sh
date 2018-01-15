#!/bin/sh
set -e
set -u

if [ "${RUN_MIGRATIONS}" = "yes" ]; then
    cd /srv/webapp
    /var/tmp/webapp/bin/python3.5 manage.py migrate --no-input
fi

uwsgi --ini /etc/uwsgi/apps-enabled/webapp.ini --uid www-data
