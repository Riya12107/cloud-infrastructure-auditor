def estimate_monthly_cost(resource_type, details=None):
    details = details or {}

    if resource_type == "ebs":
        size_gb = details.get("size", 0)
        price_per_gb = details.get("price_per_gb", 0.08)
        return round(size_gb * price_per_gb, 2)

    if resource_type == "elastic_ip":
        return 3.60

    return 0.0


def estimate_monthly_savings(resource_type, details=None):
    return estimate_monthly_cost(resource_type, details)