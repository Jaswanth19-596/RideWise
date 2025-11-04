#!/bin/bash

# log everything to start_application.log
exec > /home/ubuntu/start_application.log 2>&1

# 1. Create a user-defined bridge network
docker network create --driver bridge ridewise-net || true

# Login to ECR
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 740186513331.dkr.ecr.us-east-2.amazonaws.com

# Stop old containers
docker stop backend frontend 2>/dev/null || true
docker rm backend frontend 2>/dev/null || true

docker pull 740186513331.dkr.ecr.us-east-2.amazonaws.com/ridewise/production:backend-latest
docker pull 740186513331.dkr.ecr.us-east-2.amazonaws.com/ridewise/production:frontend-latest


# Create a secure temporary env file
ENV_FILE=$(mktemp)

# Fetch environment variables and append them to the file (Add --region and --with-decryption)
echo "DATABRICKS_HOST=$(aws ssm get-parameter --name DATABRICKS_HOST --query 'Parameter.Value' --output text --region us-east-2)" >> "$ENV_FILE"
echo "DATABRICKS_TOKEN=$(aws ssm get-parameter --name DATABRICKS_TOKEN --query 'Parameter.Value' --output text --region us-east-2 --with-decryption)" >> "$ENV_FILE"
echo "REACT_APP_API_URL=$(aws ssm get-parameter --name REACT_APP_API_URL --query 'Parameter.Value' --output text --region us-east-2)" >> "$ENV_FILE"

# Run Docker containers using the env file
docker run -d --name backend \
    --network ridewise-net \
    --env-file "$ENV_FILE" \
    -p 8000:8000 \
    740186513331.dkr.ecr.us-east-2.amazonaws.com/ridewise/production:backend-latest

docker run -d --name frontend \
    --network ridewise-net \
    --env-file "$ENV_FILE" \
    -p 80:80 \
    740186513331.dkr.ecr.us-east-2.amazonaws.com/ridewise/production:frontend-latest

rm "$ENV_FILE"