# Overview

This folder contains bash scripts to perform setup of a local environment which can be used for testing the main python script in /src dir.

## setupLocalEnv.sh

This script will setup your local environment to perform testing on the main app without having direct access to AWS. The idea behind this script is to install all of the local dependencies to get LocalStack up and running.

### Pre-Reqs

- Docker Desktop
- LocalStack CLI
- LocalStack Auth Token
- python3 + pip

LocalStack is used to mimic an AWS environment. LocalStack should already be setup/configured for this to work. If you need help setting this up, details can be found on the LocalStack site [here](https://docs.localstack.cloud/getting-started/quickstart/).

## createBuckets.sh

The createBuckets script will create a list of buckets that have been passed in along with some bucket objects that can be used during testing.

Bucket structure will be assumed as:

```bash
  s3-bucket-name
    deploy1/index.html
          /css/font.css
          /images/hey.png 
    deploy2/root.html
          /styles/font.css
          /img/hey.png 
    deploy3/base.html
          /fonts/font.css
          /png/hey.png 
```

## main.sh

This is the wrapper that ties everything together. Main is what should be kicked off as the entrypoint into creating the environment.
