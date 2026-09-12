\# Cloud Infrastructure Auditor



A Python CLI application for auditing cloud infrastructure and

identifying unused or underutilized resources for cost optimization.



\## Project Objective



The application audits cloud infrastructure, identifies unused or

underutilized resources, reports potential savings, and provides

safe cleanup operations.



\## Technology Stack



\- Python

\- Typer

\- Rich

\- Boto3

\- PyYAML

\- JSON

\- Python Dotenv



\## Project Structure



```text

cloud-infrastructure-auditor/

│

├── src/

│   ├── cli/

│   ├── auth/

│   ├── scanners/

│   ├── reports/

│   ├── cleanup/

│   ├── config/

│   └── utils/

│

├── tests/

│   ├── unit/

│   └── integration/

│

├── docs/

│

├── README.md

├── requirements.txt

├── .env.example

└── .gitignore

