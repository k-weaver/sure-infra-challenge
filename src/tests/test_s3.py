import os
import boto3
import pytest
from moto import mock_aws
from helpers.aws.s3 import S3Manager


@pytest.fixture(scope="function", name="aws_credentials")
def setup_aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture(scope="function", name="s3_client")
def setup_s3_client(aws_credentials):
    """Setup the S3 client."""
    with mock_aws():
        conn = boto3.client("s3", region_name="us-east-1")
        yield conn


@pytest.fixture(scope="function", name="s3_bucket")
def setup_s3_bucket(s3_client):
    """Setup the S3 bucket with objects."""
    bucket_name = "sure-app-test-bucket"
    s3_client.create_bucket(Bucket=bucket_name)
    s3_client.put_object(Bucket=bucket_name, Key="deploy1/2024-01-01/index.html")
    s3_client.put_object(Bucket=bucket_name, Key="deploy2/2024-01-02/index.html")
    s3_client.put_object(Bucket=bucket_name, Key="files/2024-01-03/index.html")
    return bucket_name


def test_get_s3_buckets(s3_client, s3_bucket):
    """Verifies that the get_s3_buckets method returns the correct list of S3 buckets."""
    bucket_name = s3_bucket

    manager = S3Manager(endpoint=None, s3_client=s3_client)
    buckets = manager.get_s3_buckets()

    assert bucket_name in buckets


def test_get_deployment_dirs(s3_client, s3_bucket):
    """Verifies the that the get_deployment_dirs method returns the correct list of deployment directories."""
    bucket_name = s3_bucket

    manager = S3Manager(endpoint=None, s3_client=s3_client)
    deployment_dirs = manager.get_deployment_dirs(
        bucket_name=bucket_name, days_to_check=-1
    )

    assert "sure-app-test-bucket/deploy1" in deployment_dirs
    assert "sure-app-test-bucket/deploy2" in deployment_dirs
    assert "sure-app-test-bucket/files" not in deployment_dirs


def test_delete_deployment_objects(s3_client, s3_bucket):
    """Verifies that the delete_deployment_objects method deletes the correct objects."""
    bucket_name = s3_bucket

    objects_to_delete = [
        f"{bucket_name}/deploy1",
        f"{bucket_name}/deploy2",
    ]

    manager = S3Manager(endpoint=None, s3_client=s3_client)
    manager.delete_deployment_objects(objects_to_delete, dry_run=True)
    objects = s3_client.list_objects(Bucket=bucket_name)
    assert len(objects["Contents"]) == 3

    manager.delete_deployment_objects(objects_to_delete, dry_run=False)
    objects = s3_client.list_objects(Bucket=bucket_name)
    assert len(objects["Contents"]) == 1
