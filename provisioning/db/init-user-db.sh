#!/bin/bash
set -e
set -u

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER webapp;
    CREATE DATABASE webapp;
    GRANT ALL PRIVILEGES ON DATABASE webapp TO webapp;
    ALTER USER webapp WITH PASSWORD 'na9Chie9Phie6Yeepae1aech';
EOSQL
