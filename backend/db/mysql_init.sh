
#!/bin/sh
set -e
set -u

create_database() {
    mysql -h "$MYSQL_HOST" -P 3306 -u "$MYSQL_USER" -p"$MYSQL_PASSWORD"<<-EOSQL
    CREATE DATABASE IF NOT EXISTS $MYSQL_DB
    \q
EOSQL
}

connect_database() {
    mysql -h "$MYSQL_HOST" -P 3306 -u "$MYSQL_USER" -p"$MYSQL_PASSWORD"<<-EOSQL
    \q
EOSQL
}

create_database
connect_database