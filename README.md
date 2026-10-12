# Cloud Infrastructure Auditor & Cost Optimizer

## 1. Project Overview

Cloud Infrastructure Auditor & Cost Optimizer is a Python command-line application designed to help identify potentially unused, underutilized, or cost-inefficient cloud resources.

The application supports AWS and Google Cloud Platform (GCP). It scans supported resources, analyzes findings, provides recommendations, estimates potential monthly savings, and generates reports.

The cleanup preview provides recommendations only. It does not automatically delete, release, or modify cloud resources.

## 2. Features

- Command-line interface built with Typer.
- YAML-based configuration.
- AWS integration using Boto3.
- Google Cloud Compute integration.
- Scanning for supported EC2, EBS, Elastic IP, S3, and GCP Compute resources.
- Identification of selected resource utilization and configuration issues.
- Potential monthly cost-saving estimates.
- Rich terminal audit reports.
- JSON report export.
- Safe cleanup preview.
- Automated tests using pytest.
- Logging and error handling.

**Note:** Resource coverage depends on the selected provider and implemented scanners. Cost estimates are approximate and should not be treated as actual cloud billing amounts.

## 3. Technology Stack

- Python 3.13
- Typer
- Rich
- Boto3
- Google Cloud Compute Python library
- PyYAML
- pytest
- JSON

## 4. Project Setup

### Prerequisites

- Python installed on your computer.
- Git, if cloning the repository.
- Cloud credentials and permissions for live cloud scans.

### Install dependencies

Clone the repository and open the project directory. Create and activate a virtual environment if you do not already have one.

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the required packages:

```powershell
python -m pip install -r requirements.txt
```

If PowerShell blocks virtual-environment activation, use the Python executable from the virtual environment directly or follow your organization's execution-policy guidance.

## 5. Configuration

Edit `config/config.yaml`:

```yaml
provider: aws
region: ap-south-1

gcp:
  project_id: ""
  zone: "asia-south1-a"

thresholds:
  ec2_cpu: 10
```

- `provider`: Select `aws` or `gcp`.
- `region`: AWS region used for AWS scans.
- `gcp.project_id`: Required when using GCP.
- `gcp.zone`: Configured GCP Compute zone.
- `thresholds.ec2_cpu`: EC2 CPU utilization threshold, from 0 to 100.

The application validates key configuration values before running an audit.

## 6. Cloud Credentials

### AWS

Configure AWS credentials using an approved method, such as the AWS CLI:

```powershell
aws configure
```

Use credentials with the read permissions required by the scanners. Do not commit access keys, secret keys, or other credentials to GitHub.

### Google Cloud Platform

Configure Google Cloud authentication and provide a valid project ID when selecting GCP. Ensure the authenticated identity has the permissions needed to list and inspect Compute Engine resources.

## 7. Running the Application

Display available commands:

```powershell
python -m app.main --help
```

Start the application:

```powershell
python -m app.main start
```

Display project information:

```powershell
python -m app.main info
```

Display the application version:

```powershell
python -m app.main version
```

Run a cloud audit:

```powershell
python -m app.main audit
```

Preview suggested cleanup actions:

```powershell
python -m app.main cleanup-preview
```

The cleanup preview is read-only and does not execute destructive operations.

## 8. Reports

The audit command displays a summary and findings in the terminal and exports a JSON report to `audit_report.json`.

The JSON report contains a resource summary and a list of findings. The exact findings depend on the configured provider, accessible resources, permissions, and scan results.

If cloud credentials are missing or access is denied, review the logs and configure the required permissions. An empty report does not prove that the cloud account contains no resources.

## 9. Running Tests

Run the complete test suite:

```powershell
python -m pytest -q
```

Run configuration validation tests:

```powershell
python -m pytest tests/test_config_loader.py -v
```

Tests verify implemented behavior and do not require a successful live cloud scan for every test.

## 10. Safety and Limitations

- The tool provides recommendations and does not automatically clean up resources.
- Cost estimates are approximate and may differ from actual provider charges.
- Live scan results depend on valid credentials, permissions, region, project configuration, and API availability.
- A successful command execution alone does not guarantee that every cloud resource was scanned.
- Only the resource types supported by the implemented scanners are included.

## 11. Repository

GitHub repository: https://github.com/Riya12107/cloud-infrastructure-auditor