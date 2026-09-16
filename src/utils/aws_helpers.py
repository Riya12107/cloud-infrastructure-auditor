import random
import time

from botocore.exceptions import BotoCoreError, ClientError

from src.auth.aws_auth import create_aws_session


RETRYABLE_ERROR_CODES = {
    "Throttling",
    "ThrottlingException",
    "RequestLimitExceeded",
    "TooManyRequestsException",
    "ProvisionedThroughputExceededException",
    "ServiceUnavailable",
}


def create_aws_client(
    service_name: str,
    region_name: str | None = None,
):
    """
    Create a boto3 client for an AWS service.

    Uses the configured AWS region when no region is supplied.
    """

    session = create_aws_session()

    if region_name:
        return session.client(
            service_name,
            region_name=region_name,
        )

    return session.client(service_name)


def get_retry_delay(
    attempt: int,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
) -> float:
    """
    Calculate exponential backoff delay with jitter.

    Example:
        attempt 1 -> around 1 second
        attempt 2 -> around 2 seconds
        attempt 3 -> around 4 seconds

    The random jitter prevents multiple clients from
    retrying at exactly the same time.
    """

    exponential_delay = base_delay * (2 ** (attempt - 1))

    jitter = random.uniform(0, 0.25 * exponential_delay)

    return min(
        exponential_delay + jitter,
        max_delay,
    )


def is_retryable_client_error(error: ClientError) -> bool:
    """
    Check whether an AWS ClientError should be retried.
    """

    error_code = (
        error.response
        .get("Error", {})
        .get("Code", "")
    )

    return error_code in RETRYABLE_ERROR_CODES


def call_aws_api(
    api_function,
    *args,
    retries: int = 3,
    **kwargs,
):
    """
    Execute an AWS API function with retry handling.

    Retries are performed for:
    - AWS throttling
    - Request limits
    - Temporary service errors
    - BotoCore connection-level errors
    """

    for attempt in range(1, retries + 1):

        try:
            return api_function(*args, **kwargs)

        except ClientError as error:

            if not is_retryable_client_error(error):
                raise

            if attempt == retries:
                raise

            wait_time = get_retry_delay(attempt)

            print(
                f"AWS API request throttled or temporarily unavailable. "
                f"Retry {attempt}/{retries - 1} "
                f"in {wait_time:.2f} seconds..."
            )

            time.sleep(wait_time)

        except BotoCoreError:

            if attempt == retries:
                raise

            wait_time = get_retry_delay(attempt)

            print(
                f"AWS connection error. "
                f"Retry {attempt}/{retries - 1} "
                f"in {wait_time:.2f} seconds..."
            )

            time.sleep(wait_time)

    raise RuntimeError(
        "AWS API call failed after all retries."
    )