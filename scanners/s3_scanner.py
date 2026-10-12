import logging

from botocore.exceptions import BotoCoreError, ClientError

from app.aws_connection import create_aws_session

logger = logging.getLogger(__name__)


def get_s3_buckets():
    session = create_aws_session()

    if session is None:
        raise RuntimeError(
            "AWS credentials are unavailable; cannot scan S3 buckets."
        )

    try:
        s3 = session.client("s3")
        response = s3.list_buckets()

        return [
            {
                "bucket_name": bucket.get("Name"),
                "creation_date": bucket.get("CreationDate"),
            }
            for bucket in response.get("Buckets", [])
        ]

    except (BotoCoreError, ClientError):
        logger.exception("Failed to scan S3 buckets.")
        raise