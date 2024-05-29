# Overview

This folder contains scripts to perform actions related to the challenge. See below for additional details.

## setupLocalEnv.sh

This script will setup your local environment to perform testing on the main app without having direct access to AWS.

### Pre-Reqs

- Docker Desktop
- LocalStack CLI
- LocalStack Auth Token
- python3 + pip

LocalStack is used to mimic an AWS environment. LocalStack should already be setup/configured for this to work. If you need help setting this up, details can be found on the LocalStack site [here](https://docs.localstack.cloud/getting-started/quickstart/).

## S3 Bucket

Bucket structure will be assumed as:

```bash
  s3-bucket-name
    deployhash112/index.html
          /css/font.css
          /images/hey.png 
    dsfsfsl9074/root.html
          /styles/font.css
          /img/hey.png 
    delkjlkploy3/base.html
          /fonts/font.css
          /png/hey.png 
    dsfff1234321/...
    klljkjkl123/...
```
