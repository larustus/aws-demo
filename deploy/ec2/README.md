# EC2 Docker Compose Deployment

Use this Compose file on an EC2 Ubuntu server to run the already-built AWS ECR image.

## Log in to AWS ECR

```bash
aws ecr get-login-password --region eu-north-1 | docker login --username AWS --password-stdin 340528523115.dkr.ecr.eu-north-1.amazonaws.com
```

## Pull the Image

From this directory on the EC2 server:

```bash
docker compose pull
```

## Start the API

```bash
docker compose up -d
```

## Check the Container

```bash
docker compose ps
```

## View Logs

```bash
docker compose logs -f
```

## Test the API

```bash
curl http://localhost:5000/health
```
