import json
from pathlib import Path


def export_findings_to_json(
    findings: list[dict],
    output_path: str | Path,
) -> None:
    """
    Export audit findings to a JSON file.

    Args:
        findings: List of audit findings returned by scanners.
        output_path: Path where the JSON file will be created.
    """

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        mode="w",
        encoding="utf-8",
    ) as json_file:

        json.dump(
            findings,
            json_file,
            indent=4,
        )