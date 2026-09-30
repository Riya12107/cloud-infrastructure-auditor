import csv
from pathlib import Path


CSV_FIELDS = [
    "resource_type",
    "resource_id",
    "region",
    "status",
    "reason",
    "cleanup_action",
]


def export_findings_to_csv(
    findings: list[dict],
    output_path: str | Path,
) -> None:
    """
    Export audit findings to a CSV file.

    Args:
        findings: List of audit findings returned by scanners.
        output_path: Path where the CSV file will be created.
    """

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        mode="w",
        newline="",
        encoding="utf-8",
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=CSV_FIELDS,
            extrasaction="ignore",
        )

        writer.writeheader()

        for finding in findings:
            writer.writerow(
                {
                    field: finding.get(field, "")
                    for field in CSV_FIELDS
                }
            )