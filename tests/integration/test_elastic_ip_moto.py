import boto3
from moto import mock_aws
from unittest.mock import patch

from src.scanners.elastic_ip_scanner import ElasticIPScanner


@mock_aws
def test_elastic_ip_scanner_with_moto():
    session = boto3.Session(
        aws_access_key_id="testing",
        aws_secret_access_key="testing",
        region_name="us-east-1",
    )

    ec2_client = session.client("ec2")

    # Create an unassociated Elastic IP.
    unused_address = ec2_client.allocate_address(Domain="vpc")
    unused_allocation_id = unused_address["AllocationId"]

    # Create a simulated EC2 instance.
    instance_response = ec2_client.run_instances(
        ImageId="ami-12345678",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
    )

    instance_id = instance_response["Instances"][0]["InstanceId"]

    # Create and associate another Elastic IP.
    associated_address = ec2_client.allocate_address(Domain="vpc")
    associated_allocation_id = associated_address["AllocationId"]

    ec2_client.associate_address(
        AllocationId=associated_allocation_id,
        InstanceId=instance_id,
    )

    scanner = ElasticIPScanner()

    # Use the simulated EC2 client instead of real AWS.
    with patch(
        "src.scanners.elastic_ip_scanner.create_aws_client",
        return_value=ec2_client,
    ):
        findings = scanner.scan()

    # Verify that only the unassociated address is detected.
    assert len(findings) == 1
    assert findings[0]["resource_type"] == "ElasticIP"
    assert findings[0]["resource_id"] == unused_allocation_id
    assert findings[0]["region"] == "us-east-1"
    assert findings[0]["status"] == "unused"
    assert findings[0]["reason"] == "Elastic IP is unassociated"

    finding_ids = [finding["resource_id"] for finding in findings]
    assert associated_allocation_id not in finding_ids