
from unittest.mock import patch

from app.aws_connection import create_aws_session


def test_aws_session_without_credentials():
    with patch("app.aws_connection.boto3.Session") as mock_session:
        mock_session.return_value.get_credentials.return_value = None

        session = create_aws_session()

        assert session is None


def test_aws_session_uses_requested_region():
    with patch("app.aws_connection.boto3.Session") as mock_session:
        mock_session.return_value.get_credentials.return_value = object()
        mock_session.return_value.region_name = "ap-south-1"

        session = create_aws_session(region_name="ap-south-1")

        mock_session.assert_called_once_with(
            region_name="ap-south-1"
        )
        assert session is mock_session.return_value


@patch("app.aws_connection.load_config")
@patch("app.aws_connection.boto3.Session")
def test_aws_session_uses_configured_region(
    mock_session,
    mock_load_config,
):
    mock_load_config.return_value = {
        "region": "ap-south-1",
    }
    mock_session.return_value.get_credentials.return_value = object()
    mock_session.return_value.region_name = "ap-south-1"

    session = create_aws_session()

    mock_session.assert_called_once_with(
        region_name="ap-south-1"
    )
    assert session is mock_session.return_value
