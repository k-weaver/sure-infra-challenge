#!/bin/bash

# shellcheck source=/dev/null
source "$(dirname "$0")/utils/setupLocalEnv.sh"
source "$(dirname "$0")/utils/createBuckets.sh"

echo "Setting up local environment..."
setupLocalReqs

echo "Setting up S3 buckets..."
setupS3 sure-app1-static-files sure-app2-static-files

echo "Local environment setup complete, deactivating virtual environment..."
deactivateVenv