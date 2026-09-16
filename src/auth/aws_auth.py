import boto3
from botocore.exceptions import BotoCoreError, ClientError

from src.config.settings import AWS_PROFILE, AWS_REGION


def create_aws_session():
    """
    Create and return a boto3 AWS session.

    Uses AWS_PROFILE when provided.
    Otherwise boto3 uses the default AWS credential chain.
    """

    if AWS_PROFILE:
        return boto3.Session(
            profile_name=AWS_PROFILE,
            region_name=AWS_REGION,
        )

    return boto3.Session(
        region_name=AWS_REGION,
    )


def get_aws_session_info():
    """
    Return non-sensitive information about
    the current AWS session.
    """

    session = create_aws_session()

    return {
        "profile": session.profile_name or "default",
        "region": session.region_name,
    }


def get_aws_client(service_name: str):
    """
    Create a boto3 client for the requested AWS service.
    """

    session = create_aws_session()

    return session.client(service_name)


def get_aws_resource(service_name: str):
    """
    Create a boto3 resource for the requested AWS service.

    This is useful for services where the boto3 resource
    interface is convenient.
    """

    session = create_aws_session()

    return session.resource(service_name)


def validate_aws_credentials():
    """
    Validate the currently configured AWS credentials.

    Returns:
        True  -> credentials are valid
        False -> credentials are missing or invalid
    """

    try:
        session = create_aws_session()

        sts_client = session.client("sts")

        identity = sts_client.get_caller_identity()

        print(f"AWS account: {identity.get('Account')}")
        print(f"AWS ARN: {identity.get('Arn')}")

        return True

    except (BotoCoreError, ClientError) as error:
        print(f"AWS credential validation failed: {error}")
        return False