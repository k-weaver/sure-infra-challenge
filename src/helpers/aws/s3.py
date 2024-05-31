import typing
from datetime import datetime, timedelta
import pytz

import boto3

if typing.TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client


class S3Manager:
    """S3 Manager class to interact with S3 buckets and objects."""

    def __init__(self, endpoint: str | None, s3_client: "S3Client" = None):
        # This is required for testing purposes to ensure the S3 client is mocked
        # using the same client as the one passed in the test.
        if s3_client:
            self.s3_client = s3_client
        else:
            self.s3_client = self.get_s3_client(endpoint)

    @staticmethod
    def get_s3_client(endpoint: str | None) -> "S3Client":
        """Create an S3 client with the provided endpoint.
        If no endpoint is provided, the default AWS S3 client is created.

        Args:
            endpoint (str | None): The endpoint URL for the S3 client. Defaults to None.
            This is mainly used for testing with LocalStack.

        Returns:
            S3Client: The S3 client object.
        """
        return boto3.client("s3", endpoint_url=endpoint)

    def get_s3_deploy_buckets(self) -> list:
        """Get all S3 buckets with the prefix "sure-app".

        Returns:
            list: A list of S3 buckets with the prefix "sure-app".
        """
        compiled_bucket_list = []
        app_bucket_prefix = "sure-app"
        s3_bucket_list = self.s3_client.list_buckets()

        for bucket in s3_bucket_list["Buckets"]:
            if bucket["Name"].startswith(app_bucket_prefix):
                compiled_bucket_list.append(bucket["Name"])
        print(f"App buckets: {compiled_bucket_list}")
        return compiled_bucket_list

    def get_deployment_dirs(self, bucket_name: str, days_to_check: int) -> list:
        """Get all deployment directories in the S3 bucket that are older than the specified days.

        Args:
            bucket_name (str): The name of the S3 bucket to check.
            days_to_check (int): The number of days to check for older deployments.

        Returns:
            list: A list of deployment directories that are older than the specified days.
        """
        deployment_dirs = []
        time_delta = datetime.now() - timedelta(days=days_to_check)
        time_delta = time_delta.replace(tzinfo=pytz.UTC)

        s3_objects = self.s3_client.list_objects_v2(Bucket=bucket_name)
        print(f"Current bucket: {bucket_name}")
        for s3_object in s3_objects.get("Contents", []):
            last_modified = s3_object.get("LastModified", [])
            time_check = time_delta > last_modified

            if time_check:
                dir_name = bucket_name + "/" + s3_object["Key"].split("/")[0]
                if dir_name not in deployment_dirs:
                    deployment_dirs.append(dir_name)
        print(f"  -- Deployment directories ready for deletion: {deployment_dirs}")
        return deployment_dirs

    def get_oldest_deployment_dir_by_count(self, bucket_name: str, count: int) -> list:
        """Get the oldest deployment directories in the S3 bucket based on the count.

        Args:
            bucket_name (str): The name of the S3 bucket to check.
            count (int): The number of deployment directories to keep.

        Returns:
            list: A list of bucket dirs (bucketname/prefix) that should be deleted. This is the difference of the number of objects returned and the count passed.
        """
        deployment_dirs = []
        common_s3_parent_dirs = self.s3_client.list_objects_v2(
            Bucket=bucket_name, Delimiter="/"
        )["CommonPrefixes"]

        if len(common_s3_parent_dirs) <= count:
            return deployment_dirs

        common_prefixes_with_dates = []
        for prefix in common_s3_parent_dirs:
            objects = self.s3_client.list_objects_v2(
                Bucket=bucket_name, Prefix=prefix["Prefix"]
            )["Contents"]

            # Max is used here to get the latest date of the objects in the prefix.
            # This is required in instances where the deployment directory has multiple objects which are updated at different times.
            latest_date = max(obj["LastModified"] for obj in objects)
            common_prefixes_with_dates.append((prefix["Prefix"], latest_date))

        common_prefixes_with_dates.sort(key=lambda x: x[1], reverse=True)
        sorted_common_prefixes = [
            f"{bucket_name}/{prefix}" for prefix, date in common_prefixes_with_dates
        ]
        return sorted_common_prefixes[count:]

    def delete_deployment_objects(self, deployment_dirs: list, dry_run: bool) -> None:
        """Delete all objects in the deployment directories.

        Args:
            deployment_dirs (list): A list of deployment directories to delete objects from.
        """
        for deployment_dir in deployment_dirs:
            s3_bucket, s3_object_prefix = deployment_dir.split("/", 1)

            objects_to_delete = self.s3_client.list_objects_v2(
                Bucket=s3_bucket, Prefix=s3_object_prefix
            )
            print(f"Current bucket: {s3_bucket}")
            for obj in objects_to_delete.get("Contents", []):
                if not dry_run:
                    print(f"  -- Deleting object: {obj['Key']}")
                    self.s3_client.delete_object(Bucket=s3_bucket, Key=obj["Key"])
                else:
                    print(
                        f"  -- Dry-run mode enabled. Would have deleted object: {obj['Key']}"
                    )
