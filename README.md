# Secure Data Engineering Pipeline

## 1. Project Overview

The Secure Data Engineering Pipeline is a Python-based data engineering solution designed to securely process customer data through ingestion, profiling, validation, privacy transformation, data minimization, and analytical publishing.

The main objective is to protect sensitive customer information while making useful, minimized data available for analytics.

The pipeline also provides audit logging, data reconciliation, error handling, and performance monitoring.

## 2. Architecture

The project follows a modular three-layer architecture.

### Presentation Layer
- Displays pipeline execution results and summary information through the command-line interface.
- Generates profiling, validation, reconciliation, and performance reports.
- An interactive monitoring dashboard is planned as a future enhancement.

### Application Layer
- Synthetic data generation
- Data ingestion
- Data profiling
- Data validation
- Data masking and tokenization
- Data minimization
- Security validation
- Database publishing
- Reconciliation
- Audit logging
- Performance monitoring

### Data Layer
- CSV input datasets
- Validated and rejected records
- SQLite analytical database
- JSON reports
- Audit logs

## 3. Pipeline Execution Flow

The pipeline executes the following stages:

1. Generate synthetic customer data.
2. Ingest the input dataset.
3. Profile the dataset and calculate data quality metrics.
4. Validate records and identify invalid data.
5. Move rejected records into quarantine.
6. Apply configurable masking and HMAC-SHA256 tokenization.
7. Minimize the dataset by retaining only analytical fields.
8. Perform security checks before publishing.
9. Publish analytical data into SQLite.
10. Reconcile input, valid, rejected, and published record counts.
11. Record execution details in the audit log.

Each pipeline execution is tracked using a unique Run ID.

## 4. Key Features

- Synthetic customer data generation
- Configurable privacy rules
- HMAC-SHA256 tokenization
- Sensitive information masking
- Data ingestion and schema validation
- Duplicate and malformed record detection
- Null and domain validation
- Invalid record quarantine
- Data minimization
- Secure analytical publishing
- Run-level audit trail
Execution timestamps and duration tracking

Failure logging and retry scenario testing

Source-to-target reconciliation

Performance measurement

Automated test coverage

5. Technology Stack

Python 3.13

Pandas

Faker

SQLite

JSON

Pytest

6. Project Structure

secure-data-pipeline/
│
├── config/
│   └── privacy_rules.json
│
├── data/
│   ├── input/
│   ├── output/
│   └── quarantine/
│
├── logs/
│
├── reports/
│
├── src/
│   ├── __init__.py
│   ├── audit.py
│   ├── data_generator.py
│   ├── ingestion.py
│   ├── masking.py
│   ├── minimization.py
│   ├── performance.py
│   ├── profiling.py
│   ├── publishing.py
│   ├── reconciliation.py
│   ├── security.py
│   └── validation.py
│
├── tests/
│   ├── test_audit.py
│   ├── test_data_generator.py
│   ├── test_ingestion.py
│   ├── test_minimization.py
│   ├── test_pipeline_integration.py
│   ├── test_privacy_and_publishing.py
│   ├── test_reconciliation.py
│   ├── test_security.py
│   └── test_validation.py
│
├── main.py
├── README.md
├── ARCHITECTURE.md
└── requirements.txt

7. Installation and Setup

Step 1: Clone the repository

git clone https://github.com/bindhuvaddevolu/Secure-data-pipeline.git
cd Secure-data-pipeline

Step 2: Create a virtual environment

python -m venv venv

Step 3: Activate the environment (Windows)

venv\Scripts\activate

Step 4: Install dependencies

pip install -r requirements.txt

Step 5: Configure the tokenization secret

The pipeline uses the PIPELINE_TOKEN_SECRET environment variable for HMAC-based tokenization.

For Windows Command Prompt:

set PIPELINE_TOKEN_SECRET=your_demo_secret_key_at_least_32_chars

For PowerShell:

$env:PIPELINE_TOKEN_SECRET="your_demo_secret_key_at_least_32_chars"

Use a secure, randomly generated secret in real deployments. Never commit the actual secret to Git.

8. Run the Pipeline

Execute the complete pipeline:

python main.py

The pipeline generates synthetic customer data and processes it through all stages.

On successful execution, the pipeline displays:

Unique Run ID

Total input records

Valid records

Rejected records

Published records

Reconciliation status

Sample Execution Summary

========== PIPELINE SUMMARY ==========

Run ID: <unique-run-id>
Input records: 24
Valid records: 20
Rejected records: 4
Published records: 20
Reconciliation status: passed

Pipeline completed successfully!

9. Run Automated Tests

Execute all automated tests:

python -m pytest -v

The project currently includes 32 automated tests covering:

Data generation

Data ingestion

Data validation

Privacy transformations

Data minimization

Security validation

Database publishing

Reconciliation

Audit logging

Pipeline integration

Failure and retry scenarios

Latest test result: 32 passed.

10. Performance Benchmark

The pipeline was benchmarked using 100,000 synthetic customer records.

Metric

Result

Records processed

100,000

Total execution time

13.15 seconds

Peak Python-tracked memory

89.27 MB

Throughput

7,603.74 records/second

Results are from one local benchmark and may vary depending on hardware and system conditions. Memory represents Python-tracked memory, not total process memory.

11. Security Considerations

Sensitive customer fields are removed from the analytical dataset.

HMAC-SHA256 tokenization protects customer identifiers through pseudonymization.

Tokenization secrets are supplied through environment variables.

Invalid records are separated into quarantine.

Analytical data is checked before publishing.

Audit logs capture pipeline execution details.

Data reconciliation verifies source and target record counts.

Note: HMAC-SHA256 tokenization is pseudonymization, not encryption or guaranteed anonymization. The security of tokenized data also depends on protecting the secret key.

12. Future Enhancements

Interactive pipeline monitoring dashboard

Cloud storage integration

Distributed processing for larger datasets

Advanced monitoring and alerting

13. Author

Vaddevolu HimaBindu