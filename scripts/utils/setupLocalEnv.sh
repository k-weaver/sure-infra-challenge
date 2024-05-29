#!/bin/bash
# shellcheck source=/dev/null

function createVenv() {
  if [[ ! -d "localReqs" ]]; then
    echo "Virtual environment not found"
    echo "Creating virtual environment"
    python3 -m venv localReqs
  fi
  echo "Activating virtual environment"
  source localReqs/bin/activate
}

function installDependencies() {
  echo "Installing dependencies from requirements file"
  python3 -m pip install -r "$(dirname "$0")/utils/requirements.txt"
}

function deactivateVenv() {
  echo "Deactivating virtual environment"
  deactivate
}

function setupAwsEndpoint() {
  echo "Setting up (exporting) AWS environment variables for LocalStack"
  export AWS_ACCESS_KEY_ID="test"
  export AWS_SECRET_ACCESS_KEY="test"
  export AWS_DEFAULT_REGION="us-east-1"
}

function startLocalStack() {
  echo "Starting LocalStack container"

  if ! localstack start; then
    echo "localstack failed to start, ensure Docker is running and try again"
    exit 1
  fi
}

function setupLocalReqs() {
  startLocalStack
  createVenv
  installDependencies
  setupAwsEndpoint
}
