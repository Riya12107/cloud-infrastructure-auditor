
from pathlib import Path

import yaml

from utils.logger import get_logger

CONFIG_FILE = (
    Path(__file__).resolve().parent.parent
    / "config"
    / "config.yaml"
)

logger = get_logger()


def validate_config(config):
    """Validate required cloud configuration settings."""

    if not isinstance(config, dict):
        raise ValueError(
            "Configuration must contain a YAML mapping."
        )

    provider = config.get("provider")

    if not isinstance(provider, str) or provider.lower() not in {
        "aws",
        "gcp",
    }:
        raise ValueError(
            "Invalid provider. Choose 'aws' or 'gcp'."
        )

    config["provider"] = provider.lower()

    if provider.lower() == "aws":
        region = config.get("region")

        if not isinstance(region, str) or not region.strip():
            raise ValueError(
                "AWS region is required when provider is 'aws'."
            )

    thresholds = config.get("thresholds")

    if not isinstance(thresholds, dict):
        raise ValueError(
            "Configuration must include a thresholds mapping."
        )

    cpu_threshold = thresholds.get("ec2_cpu")

    if (
        isinstance(cpu_threshold, bool)
        or not isinstance(cpu_threshold, (int, float))
        or not 0 <= cpu_threshold <= 100
    ):
        raise ValueError(
            "thresholds.ec2_cpu must be a number between 0 and 100."
        )

    if provider.lower() == "gcp":
        gcp = config.get("gcp")

        if not isinstance(gcp, dict) or not isinstance(
            gcp.get("project_id"), str
        ) or not gcp["project_id"].strip():
            raise ValueError(
                "GCP project_id is required when provider is 'gcp'."
            )

    return config


def load_config():
    """Load and validate the YAML configuration."""

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file) or {}

        return validate_config(config)

    except FileNotFoundError:
        logger.error("Configuration file was not found.")
        return {}

    except yaml.YAMLError:
        logger.error("Configuration file contains invalid YAML.")
        return {}

    except (OSError, ValueError) as error:
        logger.error(f"Configuration error: {error}")
        return {}


    except OSError as error:
        logger.error(f"Unable to read configuration file: {error}")
        return {}