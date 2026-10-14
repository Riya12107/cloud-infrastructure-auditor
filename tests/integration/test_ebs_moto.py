import boto3
from moto import mock_aws

from src.scanners.ebs_scanner import EBSScanner


@mock_aws
def test_ebs_scanner_with_moto():
    """
    Test EBSScanner using Moto's simulated AWS EC2 service.

    No real AWS resources or credentials are used.
    """

    # 1. Configure fake AWS credentials for Moto.
    session = boto3.Session(
        aws_access_key_id="testing",
        aws_secret_access_key="testing",
        region_name="us-east-1",
    )

    # 2. Create an EC2 client inside the simulated AWS environment.
    ec2_client = session.client("ec2")

    # 3. Create an unattached EBS volume.
    ec2_client.create_volume(
        AvailabilityZone="us-east-1a",
        Size=1,
        VolumeType="gp3",
    )

    # 4. Create an instance and an attached EBS volume.
    instance_response = ec2_client.run_instances(
        ImageId="ami-12345678",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
    )

    instance_id = instance_response["Instances"][0]["InstanceId"]

    attached_volume = ec2_client.create_volume(
        AvailabilityZone="us-east-1a",
        Size=1,
        VolumeType="gp3",
    )

    attached_volume_id = attached_volume["VolumeId"]

    ec2_client.attach_volume(
        VolumeId=attached_volume_id,
        InstanceId=instance_id,
        Device="/dev/sdf",
    )

    # 5. Run the actual scanner using Moto's EC2 client.
    scanner = EBSScanner()

    # The scanner creates its own client, so patch the shared helper
    # to return the Moto client created above.
    from unittest.mock import patch

    with patch(
        "src.scanners.ebs_scanner.create_aws_client",
        return_value=ec2_client,
    ):
        findings = scanner.scan()

    # 6. Verify that only the unattached volume is reported.
    assert len(findings) == 1
    assert findings[0]["resource_type"] == "EBS"
    assert findings[0]["status"] == "unused"
    assert findings[0]["reason"] == "EBS volume is unattached"

    # 7. Verify that the attached volume is not reported.
    finding_ids = [finding["resource_id"] for finding in findings]
    assert attached_volume_id not in finding_ids