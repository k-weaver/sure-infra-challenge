# Description

This is a cleanup script to delete X number of deployment objects from a given S3 bucket.

## Usage

Setup a virtual environment and install poetry with the following:

```bash
  python3 -m venv s3_cleanup
  source s3_cleanup/bin/activate
  curl -sSL https://install.python-poetry.org | python3 -
```

Install the required Python modules

```bash
  poetry install
```

Run the script with the correct params

--days - This is used to overwrite the number of days the logic will look back
--endpoint - This is used for local testing, the endpoint should be your localhost (see example)
--dry-run - This is a flag used to show what would be deleted without actually taking action

Example running the script against a LocalStack for testing:

```bash
  python3 src/main.py --days 10 --endpoint "http://localhost:4566" --dry-run
```
