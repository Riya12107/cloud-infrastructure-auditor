import json
from dataclasses import asdict


def export_json_report(result, output_file="audit_report.json"):
    """Export the audit summary, findings, status, and errors to JSON."""

    report = {
        "status": result.get("status", "success"),
        "summary": result.get("summary", {}),
        "findings": [
            asdict(finding)
            for finding in result.get("findings", [])
        ],
        "errors": result.get("errors", []),
    }

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, default=str)

    return output_file
