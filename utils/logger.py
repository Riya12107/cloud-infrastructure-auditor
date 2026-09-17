import logging
from pathlib import Path


LOG_FILE = Path(__file__).resolve().parent.parent / "auditor.log"


def get_logger(name="cloud_auditor"):
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(LOG_FILE)

        formatter = logging.Formatter(
            "%(levelname)s: %(message)s"
        )

        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger