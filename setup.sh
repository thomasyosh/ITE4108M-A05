#!/bin/sh
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done

sudo apt-get -y update
sudo apt-get -y install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get -y update

sudo apt-get install -y docker-ce
sudo apt-get install -y docker-ce-cli
sudo apt-get install -y containerd.io
sudo apt-get install -y docker-buildx-plugin
sudo apt-get install -y docker-compose-plugin

sudo systemctl enable docker

sudo groupadd docker
sudo usermod -aG docker $USER
sudo chown $USER /var/run/docker.sock
newgrp docker

. ./.env

if [ "$DATABASE_TYPE" = "postgres" ] && [ "$LOCAL_DB" = "no" ]; then
    docker run -v ./backend/db/init.sh:/init.sh --env-file .env --rm postgres:17.0-alpine ./init.sh
    echo "$DATABASE_TYPE" database init completed;
fi

if [ "$DATABASE_TYPE" = "mysql" ] && [ "$LOCAL_DB" = "no" ]; then
    docker run -v ./backend/db/mysql_init.sh:/mysql_init.sh --env-file .env --rm mysql_init:latest ./mysql_init.sh
    docker rmi $(docker images 'mysql' -a -q)
    echo "$DATABASE_TYPE" database init completed;
fi

