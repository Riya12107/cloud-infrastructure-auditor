from unittest.mock import Mock, patch

from botocore.exceptions import ClientError

from src.auth.aws_auth import (
    create_aws_session,
    get_aws_session_info,
    get_aws_client,
    get_aws_resource,
    validate_aws_credentials,
)


def test_create_aws_session_with_profile():
    with patch(
        "src.auth.aws_auth.boto3.Session"
    ) as mock_session:

        create_aws_session()

        mock_session.assert_called_once_with(
            profile_name="cloud-auditor",
            region_name="us-east-1",
        )


def test_get_aws_session_info():
    mock_session = Mock()
    mock_session.profile_name = "cloud-auditor"
    mock_session.region_name = "us-east-1"

    with patch(
        "src.auth.aws_auth.create_aws_session",
        return_value=mock_session,
    ):
        result = get_aws_session_info()

    assert result == {
        "profile": "cloud-auditor",
        "region": "us-east-1",
    }


def test_get_aws_client():
    mock_session = Mock()
    mock_client = Mock()

    mock_session.client.return_value = mock_client

    with patch(
        "src.auth.aws_auth.create_aws_session",
        return_value=mock_session,
    ):
        result = get_aws_client("ec2")

    assert result == mock_client
    mock_session.client.assert_called_once_with("ec2")


def test_get_aws_resource():
    mock_session = Mock()
    mock_resource = Mock()

    mock_session.resource.return_value = mock_resource

    with patch(
        "src.auth.aws_auth.create_aws_session",
        return_value=mock_session,
    ):
        result = get_aws_resource("ec2")

    assert result == mock_resource
    mock_session.resource.assert_called_once_with("ec2")


def test_validate_aws_credentials_success():
    mock_session = Mock()
    mock_sts_client = Mock()

    mock_sts_client.get_caller_identity.return_value = {
        "Account": "123456789012",
        "Arn": "arn:aws:iam::123456789012:user/test-user",
    }

    mock_session.client.return_value = mock_sts_client

    with patch(
        "src.auth.aws_auth.create_aws_session",
        return_value=mock_session,
    ):
        result = validate_aws_credentials()

    assert result is True
    mock_sts_client.get_caller_identity.assert_called_once()


def test_validate_aws_credentials_failure():
    mock_session = Mock()
    mock_sts_client = Mock()

    error_response = {
        "Error": {
            "Code": "InvalidClientTokenId",
            "Message": "The security token included in the request is invalid.",
        }
    }

    mock_sts_client.get_caller_identity.side_effect = ClientError(
        error_response,
        "GetCallerIdentity",
    )

    mock_session.client.return_value = mock_sts_client

    with patch(
        "src.auth.aws_auth.create_aws_session",
        return_value=mock_session,
    ):
        result = validate_aws_credentials()

    assert result is False