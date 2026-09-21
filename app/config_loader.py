from pathlib import Path
import yaml

from utils.logger import get_logger

CONFIG_FILE = Path(__file__).resolve().parent.parent / "config" / "config.yaml"

logger = get_logger()


def load_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {}

    except FileNotFoundError:
        logger.error("Configuration file was not found.")
        return {}

    except yaml.YAMLError:
        logger.error("Configuration file contains invalid YAML.")
        return {}

    except OSError as error:
        logger.error(f"Unable to read configuration file: {error}")
        return {}