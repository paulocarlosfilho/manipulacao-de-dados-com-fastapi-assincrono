#!/bin/bash
# Script de automação para deploy na AWS EC2 (User Data)
# Este script instala o Docker e sobe a aplicação automaticamente.

# Atualiza o sistema
yum update -y

# Instala o Docker
amazon-linux-extras install docker -y
service docker start
usermod -a -G docker ec2-user

# Instala o Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Cria o diretório da aplicação
mkdir -p /home/ec2-user/app
cd /home/ec2-user/app

# Aqui você clonaria seu repositório Git real
# git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git .

# Como exemplo, vamos subir o docker-compose diretamente
# docker-compose up -d
