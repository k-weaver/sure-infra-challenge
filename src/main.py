import argparse
from helpers.aws.s3 import S3Manager


def main(deployments_to_keep: int, endpoint_url: str | None, dry_run: bool):
    """Get all S3 buckets and delete deployment objects older than X days."""
    s3_manager = S3Manager(endpoint=endpoint_url)

    buckets = s3_manager.get_s3_deploy_buckets()
    for bucket in buckets:
        deployment_dirs = s3_manager.get_oldest_deployment_dir_by_count(
            bucket, count=deployments_to_keep
        )
        if not deployment_dirs:
            print(f"No deployments to delete in bucket: {bucket}")
            continue
        else:
            s3_manager.delete_deployment_objects(deployment_dirs, dry_run=dry_run)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--deployments-to-keep",
        type=int,
        default=5,
        help="Number of deployments to retain in the S3 bucket.",
    )
    parser.add_argument(
        "--endpoint",
        type=str,
        default=None,
        help="The endpoint URL for the S3 client. Defaults to None. This is mainly used for testing with LocalStack.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run the script in dry-run mode. When enabled; This will not delete any objects but will print the objects that would have been deleted. Defaults to False.",
    )
    args = parser.parse_args()
    main(
        deployments_to_keep=args.deployments_to_keep,
        endpoint_url=args.endpoint,
        dry_run=args.dry_run,
    )
