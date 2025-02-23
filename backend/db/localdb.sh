#!/bin/sh
set -e
set -u

create_database() {
    PGPASSWORD="$POSTGRES_PASSWORD" psql -h "localdb" -p "5432" -U "$POSTGRES_USER"<<-EOSQL
    SELECT 'CREATE DATABASE "$POSTGRES_DB"'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$POSTGRES_DB')\gexec
EOSQL
}

create_table() {
    PGPASSWORD="$POSTGRES_PASSWORD" psql -h "localdb" -p "5432" -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<-EOSQL
    \i backend/db/schema.sql
EOSQL
}

connect_database() {
    PGPASSWORD="$POSTGRES_PASSWORD" psql -h "localdb" -p "5432" -U "$POSTGRES_USER" -d "$POSTGRES_DB"
}

create_database
create_table
connect_database
