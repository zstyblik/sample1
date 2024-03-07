#!/bin/sh
set -e
set -u

if [ "${RUN_MIGRATIONS}" = "yes" ]; then
    cd /srv/webapp
    /var/tmp/webapp/bin/python3 manage.py migrate --no-input
fi

/var/tmp/webapp/bin/gunicorn \
    -c configs/gunicorn/conf.py \
    webapp.wsgi:application
