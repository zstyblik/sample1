FROM postgres:15.6
MAINTAINER Nobody <nobody@example.com>

ENV PGDATA=/var/lib/postgresql/data/pgdata
VOLUME /var/lib/postgresql/data/pgdata

EXPOSE 5432

RUN mkdir -p /docker-entrypoint-initdb.d /etc/postgresql
ADD init-user-db.sh /docker-entrypoint-initdb.d/init-user-db.sh
