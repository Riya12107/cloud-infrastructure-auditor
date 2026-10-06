from google.auth import default
from google.auth.exceptions import DefaultCredentialsError
from google.cloud import compute_v1

from utils.logger import get_logger

logger = get_logger()


def create_gcp_compute_client():
    try:
        credentials, project_id = default()

        if not project_id:
            logger.error("GCP project ID was not found.")
            return None

        client = compute_v1.InstancesClient(credentials=credentials)

        logger.info("GCP Compute client created successfully.")
        return client

    except DefaultCredentialsError:
        logger.error("GCP credentials were not found.")
        return None