FROM debian:stretch
MAINTAINER Nobody <nobody@example.com>

RUN \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
        libpq-dev python3.5 python3-virtualenv virtualenv \
        uwsgi uwsgi-plugin-python3

COPY webapp /srv/webapp

RUN \
    virtualenv -p python3.5 /var/tmp/webapp && \
    /var/tmp/webapp/bin/pip3.5 install -r /srv/webapp/requirements.txt

COPY docker/uwsgi/webapp.ini /etc/uwsgi/apps-enabled/
COPY docker/webapp/run.sh /var/tmp/webapp/bin/run-webapp.sh

ENTRYPOINT /var/tmp/webapp/bin/run-webapp.sh

EXPOSE 3031
