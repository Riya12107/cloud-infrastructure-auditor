# Cloud Infrastructure Auditor & Cost Optimizer



A Python-based command-line tool that audits AWS cloud infrastructure, identifies unused or underutilized resources, estimates potential cost savings, and supports safe resource cleanup.



## Project Objective



The goal of this project is to help users understand their cloud resource usage, identify potential waste, and make informed decisions about reducing cloud costs.



## Technology Stack



* **Python** — Core programming language

* **Typer** — Command-line interface

* **Rich** — Formatted terminal output

* **Boto3** — AWS SDK for Python

* **PyYAML** — YAML configuration support

* **Python-dotenv** — Environment variable configuration

* **Pytest** — Automated testing

* **Moto** — Mock AWS services for testing

* **PyInstaller** — Standalone executable generation



## Features



* Command-line interface for running audits

* AWS configuration management

* Detection of potentially unused cloud resources

* EBS volume and Elastic IP auditing

* Automated unit and integration tests

* Mock AWS testing using Moto

* Standalone Windows executable support



> Note: Actual audit coverage and cost estimates depend on the implemented scanners and their supported resources. Verify findings in your AWS account before taking action.



## Project Structure



```text

Cloud-Infrastructure-Auditor/

â”œâ”€â”€ src/

â”‚   â”œâ”€â”€ cli/

â”‚   â”‚   â””â”€â”€ main.py

â”‚   â”œâ”€â”€ auth/

â”‚   â”œâ”€â”€ config/

â”‚   â”œâ”€â”€ scanners/

â”‚   â””â”€â”€ utils/

â”œâ”€â”€ tests/

â”‚   â”œâ”€â”€ unit/

â”‚   â””â”€â”€ integration/

â”œâ”€â”€ reports/

â”œâ”€â”€ pyproject.toml

â”œâ”€â”€ requirements.txt

â”œâ”€â”€ README.md

â””â”€â”€ .gitignore

```



The exact contents of each directory may change as development continues.



## Requirements



For running from source:



* Python 3.10 or newer

* pip

* AWS credentials for live AWS audits



For building the Windows executable:



* Windows

* The project virtual environment

* PyInstaller



## Installation from Source



### 1. Clone the repository



```powershell

git clone https://github.com/Riya12107/cloud-infrastructure-auditor.git

cd cloud-infrastructure-auditor

```



### 2. Create and activate a virtual environment



```powershell

python -m venv venv

.\venv\Scripts\Activate.ps1

```



### 3. Install dependencies



```powershell

python -m pip install -r requirements.txt

python -m pip install -e .

```



## CLI Commands



### Display help



```powershell

cloud-auditor --help

```



Alternatively, run:



```powershell

python -m src.cli.main --help

```



### Display the version



```powershell

cloud-auditor version

```



Alternatively:



```powershell

python -m src.cli.main version

```



### Display configuration



```powershell

cloud-auditor config

```



### Run an audit



```powershell

cloud-auditor audit

```



Alternatively:



```powershell

python -m src.cli.main audit

```



An audit requires valid AWS credentials and appropriate permissions when accessing real AWS resources. Available scanners determine which resources are inspected.



## AWS Configuration



The application supports AWS configuration through environment variables.



| Variable      | Purpose                | Default                           |

| ------------- | ---------------------- | --------------------------------- |

| `AWS_PROFILE` | AWS CLI profile to use | Default credential chain if unset |

| `AWS_REGION`  | AWS region to audit    | `us-east-1`                       |



For example, in PowerShell:



```powershell

$env:AWS_PROFILE = "cloud-auditor"

$env:AWS_REGION = "us-east-1"

```



The profile must already be configured with valid AWS credentials. You can configure a profile using the AWS CLI:



```powershell

aws configure --profile cloud-auditor

```



Never commit AWS access keys, secret keys, session tokens, or other credentials to GitHub. Keep secrets out of source code and shared configuration files.



## Testing



Run the complete test suite:



```powershell

python -m pytest -v

```



The project includes unit tests and Moto-based integration tests that simulate AWS services without requiring live AWS resources.



## Build the Windows Executable



Install PyInstaller in the active virtual environment:



```powershell

python -m pip install pyinstaller

```



Build the executable:



```powershell

pyinstaller --clean --onefile --name cloud-auditor --collect-submodules src.cli src\cli\main.py

```



The executable will be generated at:



```text

dist\cloud-auditor.exe

```



### Test the executable



```powershell

.\dist\cloud-auditor.exe --help

.\dist\cloud-auditor.exe version

.\dist\cloud-auditor.exe config

```



Live AWS audits still require valid credentials and suitable AWS permissions. Do not assume that credentials are embedded in the executable.



## Safe Resource Cleanup



Review audit results carefully before cleaning up resources. Confirm that a resource is unused and is not required by a production workload.



Use dry-run or review modes when the application supports them. Never perform destructive cleanup based only on an estimated saving.



## Current Development Status



* Project structure and Git repository configured

* Typer CLI and configuration system implemented

* Version and audit commands implemented

* EBS and Elastic IP scanners developed

* Unit and Moto-based integration tests implemented

* Python package configuration created

* Wheel package built and tested

* Windows executable generated and tested

* README and distribution documentation in progress



## Future Improvements



* Expand supported AWS resource scanners

* Improve cost estimation accuracy

* Enhance audit report formats

* Add more test coverage

* Improve executable distribution and release documentation



## Repository



GitHub: https://github.com/Riya12107/cloud-infrastructure-auditor



## Disclaimer



This tool is intended to assist with cloud auditing and cost optimization. Audit findings and savings estimates are informational and may not reflect actual billing savings. Always verify resources, permissions, and potential impacts before making infrastructure changes.
