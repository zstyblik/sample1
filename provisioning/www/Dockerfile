FROM python:3.11-bookworm
MAINTAINER Nobody <nobody@example.com>

RUN \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
        libpq-dev python3-virtualenv virtualenv

COPY webapp /srv/webapp

RUN \
    virtualenv -p python3 /var/tmp/webapp && \
    /var/tmp/webapp/bin/pip3 install -r /srv/webapp/requirements.txt

COPY docker/webapp/run.sh /var/tmp/webapp/bin/run-webapp.sh

WORKDIR /srv/webapp

ENTRYPOINT /var/tmp/webapp/bin/run-webapp.sh

EXPOSE 3031
