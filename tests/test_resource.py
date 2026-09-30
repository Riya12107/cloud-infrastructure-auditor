from models.resource import CloudResource


def test_cloud_resource_creation():
    resource = CloudResource(
        provider="aws",
        resource_type="ec2",
        resource_id="i-test123",
        details={
            "instance_type": "t3.micro",
            "state": "running",
        },
    )

    assert resource.provider == "aws"
    assert resource.resource_type == "ec2"
    assert resource.resource_id == "i-test123"
    assert resource.details["instance_type"] == "t3.micro"