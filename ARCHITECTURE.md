
# Secure Data Pipeline Architecture

## Three-Tier Architecture

### 1. Presentation Tier
- Dashboard for viewing pipeline results.
- Displays validation reports and performance metrics.
- Planned for implementation.

### 2. Application Tier
Python modules responsible for:
- Data generation
- Data ingestion
- Data profiling
- Data validation
- Data masking and tokenization
- Data minimization
- Reconciliation
- Database publishing
- Audit logging

### 3. Data Tier
Stores pipeline data and results:
- data/input: Raw input datasets
- data/quarantine: Rejected records
- data/output: Analytical datasets and SQLite database
- reports: Profiling and validation reports
- logs: Audit logs

## Data Flow

1. Generate synthetic customer data.
2. Ingest and check the schema.
3. Profile the dataset.
4. Validate records.
5. Move invalid records to quarantine.
6. Mask and tokenize sensitive fields.
7. Minimize the dataset.
8. Reconcile record counts.
9. Publish analytical data to SQLite.
10. Record audit events.
