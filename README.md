# Cloud Infrastructure Auditor & Cost Optimizer

## Objective

A CLI tool that audits cloud infrastructure, identifies
unused or underutilized resources, estimates potential savings,
and provides safe cleanup commands.

## Technology Stack

- Python
- Typer
- Rich
- Boto3
- PyYAML
- Python-dotenv
- Pytest
- Moto
- PyInstaller

## Current Progress

Day 1:
- Project structure created
- Git repository configured
- Configuration system created
- Typer CLI created
- Audit command created
- Version command created
- Initial unit tests created

## CLI Commands

python -m src.cli.main --help

python -m src.cli.main version

python -m src.cli.main audit