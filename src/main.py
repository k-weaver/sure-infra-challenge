import os
import typing
from datetime import datetime, timedelta
import pytz

import boto3

if typing.TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client


def s3_client(endpoint: str | None) -> "S3Client":
    return boto3.client("s3", endpoint_url=endpoint)


def get_s3_buckets() -> list:
    compiled_bucket_list = []
    app_bucket_prefix = "sure-app"
    s3_bucket_list = S3_CLIENT.list_buckets()

    for bucket in s3_bucket_list["Buckets"]:
        if bucket["Name"].startswith(app_bucket_prefix):
            compiled_bucket_list.append(bucket["Name"])
    print(f"App buckets: {compiled_bucket_list}")
    return compiled_bucket_list


def get_deployment_dirs(bucket_name: str, days_to_check: int) -> list:
    deployment_dirs = []
    # timedelta set to milliseconds for testing, this should be set to days or weeks
    time_delta = datetime.now() - timedelta(days=days_to_check)

    # Convert time_delta to offset-aware
    time_delta = time_delta.replace(tzinfo=pytz.UTC)

    s3_objects = S3_CLIENT.list_objects_v2(Bucket=bucket_name)
    print(f"Current bucket: {bucket_name}")
    for s3_object in s3_objects.get("Contents", []):
        last_modified = s3_object.get("LastModified", [])

        # Check if the object was last modified before the time_delta
        # This is crucial piece of logic to determine if the object is ready for deletion
        # Use extreme caution when modifying this logic
        time_check = last_modified > time_delta

        if time_check:
            dirName = bucket_name + "/" + s3_object["Key"].split("/")[0]
            if dirName not in deployment_dirs:
                deployment_dirs.append(dirName)
    print(f"  -- Deployment directories ready for deletion: {deployment_dirs}")
    return deployment_dirs


def delete_deployment_objects(deployment_dirs: list) -> None:
    for deployment_dir in deployment_dirs:
        s3_bucket = deployment_dir.split("/")[0]
        s3_object_prefix = deployment_dir.split("/")[1]

        objets_to_delete = S3_CLIENT.list_objects_v2(
            Bucket=s3_bucket, Prefix=s3_object_prefix
        )
        print(f"Current bucket: {s3_bucket}")
        for obj in objets_to_delete.get("Contents", []):
            print(f"  -- Deleting object: {obj['Key']}")


def setup_local_aws_credentials() -> None | str:
    endpoint = None
    if os.getenv("STAGE") == "local":
        endpoint = "http://localhost:4566"
        return endpoint


def main():
    # ENDPOINT_URL = setup_local_aws_credentials()
    # S3_CLIENT = s3_client("http://localhost:4566")
    deployments_to_delete = []
    s3_bucket_list = get_s3_buckets()

    for s3_bucket in s3_bucket_list:
        deployments_to_delete.extend(get_deployment_dirs(s3_bucket, 45))
    delete_deployment_objects(deployments_to_delete)


ENDPOINT_URL = setup_local_aws_credentials()
S3_CLIENT = s3_client("http://localhost:4566")
main()
