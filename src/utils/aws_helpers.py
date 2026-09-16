import time

from botocore.exceptions import BotoCoreError, ClientError

from src.auth.aws_auth import create_aws_session


def create_aws_client(
    service_name: str,
    region_name: str = "us-east-1"
):
    """
    Create a boto3 client for an AWS service.
    """

    session = create_aws_session()

    return session.client(
        service_name,
        region_name=region_name
    )


def call_aws_api(
    api_function,
    *args,
    retries: int = 3,
    **kwargs
):
    """
    Execute an AWS API function with retry handling.

    Retries are used for temporary AWS API failures
    such as throttling or connection-related errors.
    """

    for attempt in range(1, retries + 1):

        try:
            return api_function(*args, **kwargs)

        except ClientError as error:

            error_code = error.response.get(
                "Error",
                {}
            ).get(
                "Code",
                ""
            )

            retryable_errors = {
                "Throttling",
                "ThrottlingException",
                "RequestLimitExceeded",
                "TooManyRequestsException",
                "ProvisionedThroughputExceededException",
            }

            if error_code not in retryable_errors:
                raise

            if attempt == retries:
                raise

            wait_time = 2 ** (attempt - 1)

            print(
                f"AWS API throttled. "
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)

        except BotoCoreError:

            if attempt == retries:
                raise

            wait_time = 2 ** (attempt - 1)

            print(
                f"AWS API error. "
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)

    raise RuntimeError("AWS API call failed after all retries.")