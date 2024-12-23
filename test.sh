#!bash

. ./.env

if [ "$DATABASE_TYPE" = "postgres" ] && [ "$LOCAL_DB" = "no" ]; then
    docker run -v ./backend/db/init.sh:/init.sh --env-file .env --rm postgres:latest ./init.sh
    docker rmi $(docker images 'postgres' -a -q)
    echo "$DATABASE_TYPE" database init completed;
fi

if [ "$DATABASE_TYPE" = "mysql" ] && [ "$LOCAL_DB" = "no" ]; then
    docker run -v ./backend/db/mysql_init.sh:/mysql_init.sh --env-file .env --rm mysql_init:latest ./mysql_init.sh
    docker rmi $(docker images 'mysql' -a -q)
    echo "$DATABASE_TYPE" database init completed";
fi

if [ "$LOCAL_DB" = "yes" ]; then
    docker run -v ./backend/db/localdb.sh:/localdb.sh --env-file .env --rm postgres:latest ./localdb.sh
    docker rmi $(docker images 'postgres' -a -q)
    echo "$DATABASE_TYPE" database init completed;
fi