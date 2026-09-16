from pathlib import Path
import yaml

CONFIG_FILE = Path(__file__).resolve().parent.parent / "config" / "config.yaml"


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}