from botocore.exceptions import BotoCoreError, ClientError
from app.aws_connection import create_aws_session


def get_s3_buckets():
    session = create_aws_session()

    if session is None:
        return []

    try:
        s3 = session.client("s3")

        response = s3.list_buckets()

        buckets = []

        for bucket in response.get("Buckets", []):
            buckets.append({
                "bucket_name": bucket.get("Name"),
                "creation_date": bucket.get("CreationDate"),
            })

        return buckets

    except (BotoCoreError, ClientError):
        return []