import boto3
from botocore.exceptions import NoCredentialsError

from utils.logger import get_logger

logger = get_logger()


def create_aws_session():
    try:
        session = boto3.Session()

        credentials = session.get_credentials()

        if credentials is None:
            logger.error("AWS credentials were not found.")
            return None

        logger.info("AWS session created successfully.")
        return session

    except NoCredentialsError:
        logger.error("AWS credentials were not found.")
        return None