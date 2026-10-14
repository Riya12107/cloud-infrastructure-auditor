
import boto3
from botocore.exceptions import NoCredentialsError

from app.config_loader import load_config
from utils.logger import get_logger

logger = get_logger()


def create_aws_session(region_name=None):
    """Create an AWS session using the requested or configured region."""

    try:
        if region_name is None:
            config = load_config()
            region_name = config.get("region") if config else None

        session = boto3.Session(region_name=region_name)

        credentials = session.get_credentials()

        if credentials is None:
            logger.error("AWS credentials were not found.")
            return None

        logger.info(
            "AWS session created successfully in region %s.",
            session.region_name,
        )
        return session

    except NoCredentialsError:
        logger.error("AWS credentials were not found.")
        return None
