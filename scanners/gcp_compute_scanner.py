from app.gcp_connection import create_gcp_compute_client
from models.resource import CloudResource
from google.api_core.exceptions import GoogleAPIError


def get_gcp_compute_instances(project_id, zone):
    client = create_gcp_compute_client()

    if client is None:
        return []

    try:
        request = {
            "project": project_id,
            "zone": zone,
        }

        instances = client.list(request=request)

        resources = []

        for instance in instances:
            resources.append(
                CloudResource(
                    provider="gcp",
                    resource_type="compute_instance",
                    resource_id=instance.name,
                    details={
                        "machine_type": instance.machine_type,
                        "status": instance.status,
                        "zone": zone,
                    },
                )
            )

        return resources

    except GoogleAPIError:
        return []