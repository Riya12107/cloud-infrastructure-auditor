from app.aws_connection import create_aws_session


def get_elastic_ips():
    session = create_aws_session()

    if session is None:
        return []

    ec2 = session.client("ec2")

    response = ec2.describe_addresses()

    addresses = []

    for address in response.get("Addresses", []):
        addresses.append({
            "public_ip": address.get("PublicIp"),
            "allocation_id": address.get("AllocationId"),
            "associated": bool(address.get("AssociationId")),
        })

    return addresses