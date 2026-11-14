
# Secure Data Engineering Pipeline

## Project Overview
A Python-based secure data engineering pipeline that generates synthetic customer data, validates records, protects sensitive information, minimizes data, and publishes analytical datasets.

## Key Features
- Synthetic data generation
- Data ingestion and schema checks
- Data profiling
- Data validation and quarantine
- Configurable masking and tokenization
- Analytical data minimization
- SQLite publishing
- Append-only audit logging
- Idempotent publishing
- Automated testing
- Performance testing with 100,000 records

## Technology Stack
- Python
- Pandas
- Faker
- SQLite
- Pytest
- HMAC-SHA256

## Run the Project

Set the tokenization secret:

    set PIPELINE_TOKEN_SECRET=YourSecretKeyAtLeast32Characters

Run the pipeline:

    python main.py

Run tests:

    python -m pytest -v

Run performance test:

    python -m src.performance

## Architecture

Presentation Layer: Dashboard (planned)

Application Layer: Python pipeline modules

Data Layer: CSV files, quarantine storage, SQLite database

## Output
- Validated customer records
- Rejected records and validation report
- Masked customer dataset
- Minimized analytical dataset
- SQLite analytical database
- Audit logs
- Profiling report
- Performance report
