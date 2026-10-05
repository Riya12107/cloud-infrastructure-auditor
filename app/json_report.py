import json
from dataclasses import asdict


def export_json_report(result, output_file="audit_report.json"):
    report = {
        "summary": result.get("summary", {}),
        "findings": [
            asdict(finding)
            for finding in result.get("findings", [])
        ],
    }

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, default=str)

    return output_file