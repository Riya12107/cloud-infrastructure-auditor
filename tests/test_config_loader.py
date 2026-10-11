
import pytest

from app.config_loader import validate_config


def valid_aws_config():
    return {
        "provider": "aws",
        "region": "ap-south-1",
        "thresholds": {"ec2_cpu": 10},
        "gcp": {
            "project_id": "",
            "zone": "asia-south1-a",
        },
    }


def test_valid_aws_config_is_accepted():
    config = valid_aws_config()

    result = validate_config(config)

    assert result["provider"] == "aws"
    assert result["region"] == "ap-south-1"


def test_provider_is_normalized_to_lowercase():
    config = valid_aws_config()
    config["provider"] = "AWS"

    result = validate_config(config)

    assert result["provider"] == "aws"


def test_invalid_provider_is_rejected():
    config = valid_aws_config()
    config["provider"] = "azure"

    with pytest.raises(ValueError, match="Invalid provider"):
        validate_config(config)


def test_missing_aws_region_is_rejected():
    config = valid_aws_config()
    config["region"] = ""

    with pytest.raises(ValueError, match="AWS region is required"):
        validate_config(config)


@pytest.mark.parametrize("threshold", [-1, 101, True, "10"])
def test_invalid_cpu_threshold_is_rejected(threshold):
    config = valid_aws_config()
    config["thresholds"]["ec2_cpu"] = threshold

    with pytest.raises(ValueError, match="ec2_cpu"):
        validate_config(config)


def test_missing_gcp_project_id_is_rejected():
    config = valid_aws_config()
    config["provider"] = "gcp"

    with pytest.raises(ValueError, match="GCP project_id is required"):
        validate_config(config)


def test_valid_gcp_config_is_accepted():
    config = valid_aws_config()
    config["provider"] = "gcp"
    config["gcp"]["project_id"] = "demo-project"

    result = validate_config(config)

    assert result["provider"] == "gcp"

