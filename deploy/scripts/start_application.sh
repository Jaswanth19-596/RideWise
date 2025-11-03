#!/bin/bash

# log everything to start_application.log
exec > /home/ubuntu/start_application.log 2>&1

echo "Logging into ECR ..."
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 740186513331.dkr.ecr.us-east-2.amazonaws.com

docker build -t ridewise/production-backend ./backend
docker build -t ridewise/production-frontend ./frontend

docker tag ridewise/production-backend:latest 740186513331.dkr.ecr.us-east-2.amazonaws.com/ridewise/production-backend:latest
docker tag ridewise/production-frontend:latest 740186513331.dkr.ecr.us-east-2.amazonaws.com/ridewise/production-frontend:latest

docker push 740186513331.dkr.ecr.us-east-2.amazonaws.com/ridewise/production-backend:latest
docker push 740186513331.dkr.ecr.us-east-2.amazonaws.com/ridewise/production-frontend:latest