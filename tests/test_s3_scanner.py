from unittest.mock import patch

from scanners.s3_scanner import get_s3_buckets


@patch("scanners.s3_scanner.create_aws_session")
def test_s3_scanner_returns_bucket_data(mock_session):
    mock_s3 = mock_session.return_value.client.return_value

    mock_s3.list_buckets.return_value = {
        "Buckets": [
            {
                "Name": "test-bucket",
                "CreationDate": "2026-09-25T10:00:00Z",
            }
        ]
    }

    buckets = get_s3_buckets()

    assert len(buckets) == 1
    assert buckets[0]["bucket_name"] == "test-bucket"
    assert buckets[0]["creation_date"] == "2026-09-25T10:00:00Z"

from botocore.exceptions  import ClientError


@patch("scanners.s3_scanner.create_aws_session")
def test_s3_scanner_handles_aws_error(mock_session):
    mock_s3 = mock_session.return_value.client.return_value

    mock_s3.list_buckets.side_effect = ClientError(
        {
            "Error": {
                "Code": "AccessDenied",
                "Message": "Access denied",
            }
        },
        "ListBuckets",
    )

    buckets = get_s3_buckets()

    assert buckets == []