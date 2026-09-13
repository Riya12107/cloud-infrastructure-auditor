import time

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def create_aws_client(service_name: str, region_name: str = "us-east-1"):
    """
    Create a boto3 client for an AWS service.
    """

    return boto3.client(
        service_name,
        region_name=region_name
    )


def call_aws_api(api_function, *args, retries: int = 3, **kwargs):
    """
    Execute an AWS API call with basic retry handling.

    Retries temporary AWS/API failures before returning the error.
    """

    for attempt in range(1, retries + 1):
        try:
            return api_function(*args, **kwargs)

        except (BotoCoreError, ClientError) as error:
            if attempt == retries:
                raise

            wait_time = 2 ** (attempt - 1)

            print(
                f"AWS API call failed. "
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)