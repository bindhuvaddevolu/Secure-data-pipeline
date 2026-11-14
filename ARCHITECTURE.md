# Secure Data Pipeline Architecture

## 1. Architecture Overview

The Secure Data Engineering Pipeline follows a modular three-tier architecture. Each tier has a specific responsibility in securely processing customer data and publishing analytical information.

## 2. Three-Tier Architecture

### 1. Presentation Tier

Responsible for displaying pipeline execution information and reports.

- Command-line interface for pipeline execution.
- Displays pipeline execution summary and Run ID.
- Generates and presents validation, profiling, reconciliation, and performance reports.
- Interactive monitoring dashboard is planned for future implementation.

### 2. Application Tier

Python modules responsible for processing, validating, and securing data.

- Data generation
- Data ingestion
- Data profiling
- Data validation
- Data masking and tokenization
- Data minimization
- Security validation
- Reconciliation
- Database publishing
- Audit logging
- Performance monitoring

### 3. Data Tier

Responsible for storing input data, processed records, analytical outputs, and execution information.

- `data/input/` – Raw synthetic customer datasets.
- `data/quarantine/` – Rejected records and validation results.
- `data/output/` – Analytical datasets and SQLite databases.
- `reports/` – Profiling, validation, reconciliation, and performance reports.
- `logs/` – Pipeline audit logs.

## 3. Data Flow

The pipeline follows these execution stages:

1. Generate synthetic customer data.
2. Ingest the dataset and verify its schema.
3. Profile the dataset and calculate data quality metrics.
4. Validate records against required fields and business rules.
5. Separate invalid records into quarantine.
6. Apply configurable masking and HMAC-SHA256 tokenization.
7. Minimize the dataset by retaining only required analytical fields.
8. Perform security validation to prevent sensitive data from reaching the analytical output.
9. Publish the analytical dataset into SQLite.
10. Reconcile input, valid, rejected, and published record counts.
11. Record stage-level execution details in the audit log.

## 4. Security and Data Protection

- Sensitive customer fields are masked or removed from analytical outputs.
- Customer identifiers are tokenized using HMAC-SHA256.
- Tokenization secrets are managed through environment variables.
- Invalid records are separated from valid records.
- Security validation is performed before database publishing.
- Audit logs maintain execution details and status for each pipeline run.

**Note:** HMAC-SHA256 tokenization provides pseudonymization, not encryption or guaranteed anonymization.

## 5. Reliability and Monitoring

- Unique Run ID for every pipeline execution.
- Stage-level execution status and duration tracking.
- Failure logging and retry scenario testing.
- Source-to-target record reconciliation.
- Automated tests for successful execution and edge cases.
- Performance benchmarking for large datasets.
6. Future Enhancements

- Interactive dashboard for pipeline monitoring.

- Cloud-based data storage.

- Distributed data processing.

- Advanced alerting and monitoring.