from botocore.exceptions import ClientError

from src.utils.aws_helpers import call_aws_api


def test_call_aws_api_retries_on_throttling(monkeypatch):
    attempts = {"count": 0}

    def fake_api():
        attempts["count"] += 1

        if attempts["count"] < 3:
            raise ClientError(
                {
                    "Error": {
                        "Code": "Throttling",
                        "Message": "Rate exceeded",
                    }
                },
                "FakeApi",
            )

        return {"status": "success"}

    monkeypatch.setattr(
        "src.utils.aws_helpers.time.sleep",
        lambda seconds: None,
    )

    result = call_aws_api(
        fake_api,
        retries=3,
    )

    assert result == {"status": "success"}
    assert attempts["count"] == 3


def test_call_aws_api_does_not_retry_non_retryable_error(monkeypatch):
    attempts = {"count": 0}

    def fake_api():
        attempts["count"] += 1

        raise ClientError(
            {
                "Error": {
                    "Code": "InvalidParameterValue",
                    "Message": "Invalid parameter",
                }
            },
            "FakeApi",
        )

    monkeypatch.setattr(
        "src.utils.aws_helpers.time.sleep",
        lambda seconds: None,
    )

    try:
        call_aws_api(
            fake_api,
            retries=3,
        )
    except ClientError as error:
        assert error.response["Error"]["Code"] == "InvalidParameterValue"

    assert attempts["count"] == 1


def test_call_aws_api_stops_after_max_retries(monkeypatch):
    attempts = {"count": 0}

    def fake_api():
        attempts["count"] += 1

        raise ClientError(
            {
                "Error": {
                    "Code": "Throttling",
                    "Message": "Rate exceeded",
                }
            },
            "FakeApi",
        )

    monkeypatch.setattr(
        "src.utils.aws_helpers.time.sleep",
        lambda seconds: None,
    )

    try:
        call_aws_api(
            fake_api,
            retries=3,
        )
    except ClientError as error:
        assert error.response["Error"]["Code"] == "Throttling"

    assert attempts["count"] == 3