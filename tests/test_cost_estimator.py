from app.cost_estimator import (
    estimate_monthly_cost,
    estimate_monthly_savings,
)


def test_ebs_monthly_cost():
    cost = estimate_monthly_cost(
        "ebs",
        {"size": 100},
    )

    assert cost == 8.00


def test_elastic_ip_monthly_cost():
    cost = estimate_monthly_cost("elastic_ip")

    assert cost == 3.60


def test_unknown_resource_cost():
    cost = estimate_monthly_cost("unknown")

    assert cost == 0.0


def test_ebs_monthly_savings():
    savings = estimate_monthly_savings(
        "ebs",
        {"size": 50},
    )

    assert savings == 4.00