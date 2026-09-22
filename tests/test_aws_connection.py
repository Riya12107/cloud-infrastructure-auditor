from app.aws_connection import create_aws_session


def test_aws_session_without_credentials():
    session = create_aws_session()

    assert session is None