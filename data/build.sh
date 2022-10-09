#!/bin/bash

echo "[+] Building Gitlab"
echo "[+] OS: Ubuntu 20.04 LTS"
echo "[+] Author: Enox"

echo "[+] Configuring hostname"
hostnamectl set-hostname gitlab
cat << EOF > /etc/hosts
127.0.0.1 localhost
127.0.0.1 gitlab.example gitlab
EOF

echo "[1] Setting up Gitlab"

echo "[1.1] Installing docker"
sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
sudo apt update
sudo apt install -y docker-ce docker-compose

sudo systemctl enable docker.service
sudo systemctl enable containerd.service

echo "[1.2] Configuring gitlab container"
docker pull gitlab/gitlab-ee:15.3.1-ee.0

# Building Continaer
COMPOSE_PROJECT_NAME="gitlab"
cd /data && docker-compose up -d

# Waiting for container to be healthy before continuing [ Timeout set to 2000 seconds ]
bash /data/healthy.sh gitlab 2000


echo "[1.3] Creating personal access token and adding users"
docker exec -it gitlab gitlab-rails runner "token = User.find_by_username('root').personal_access_tokens.create(scopes: [:sudo, :api], name: 'Automation token'); token.set_token('ZtvWQhRTpzqfRzRn3bvLl59o'); token.save!"

# Creating user enox wiht password as StrongestGitlabPassword
curl --request POST --header "PRIVATE-TOKEN: ZtvWQhRTpzqfRzRn3bvLl59o" --data "skip_confirmation=true&email=enox@gitlab.example&name=Enox&username=enox&password=StrongestGitlabPassword" "http://gitlab.example/api/v4/users"

