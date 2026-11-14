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

For more architectural details, see [ARCHITECTURE.md](ARCHITECTURE.md).

## 3. Pipeline Execution Flow

The pipeline executes the following stages:

1. Generate synthetic customer data.
2. Ingest the input dataset.
3. Profile the dataset and calculate data quality metrics.
4. Validate records and identify invalid data.
5. Separate rejected records into quarantine.
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
- Execution timestamps and duration tracking
- Failure logging and retry scenario testing
- Source-to-target reconciliation
- Performance measurement
- Automated test coverage
- Source row-level traceability for rejected records
- Source file and Run ID tracking
- Rejection reason tracking
- UTC timestamps in ISO-8601 format

## 5. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.13 | Pipeline implementation |
| Pandas | Data processing |
| Faker | Synthetic data generation |
| SQLite | Analytical data publishing |
| JSON | Configuration and reports |
| Pytest | Automated testing |

## 6. Project Structure

```text
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
│   ├── data_dictionary.md
│   └── test_results.txt
│
├── samples/
│   ├── sample_input.csv
│   ├── expected_labels.csv
│   ├── sample_analytical_output.csv
│   └── sample_reconciliation.json
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
├── DESIGN_DECISIONS.md
├── requirements.txt
└── .gitignore
```

## 7. Installation and Setup

### Step 1: Clone the repository

```bash
git clone https://github.com/bindhuvaddevolu/Secure-data-pipeline.git
cd Secure-data-pipeline
```

### Step 2: Create a virtual environment

```bash
python -m venv venv
```

### Step 3: Activate the environment (Windows)

```cmd
venv\Scripts\activate
```

### Step 4: Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 5: Configure the tokenization secret

The pipeline uses the `PIPELINE_TOKEN_SECRET` environment variable for HMAC-based tokenization.

For Windows Command Prompt:

```cmd
set PIPELINE_TOKEN_SECRET=your_demo_secret_key_at_least_32_chars
```

For PowerShell:

```powershell
$env:PIPELINE_TOKEN_SECRET="your_demo_secret_key_at_least_32_chars"
```

Use a secure, randomly generated secret in real deployments. Never commit the actual secret to Git.

## 8. Run the Pipeline

Execute the complete pipeline:

```bash
python main.py
```

The pipeline generates synthetic customer data and processes it through all stages.

On successful execution, the pipeline displays:

- Unique Run ID
- Total input records
- Valid records
- Rejected records
- Published records
- Reconciliation status

### Sample Execution Summary

```text
========== PIPELINE SUMMARY ==========

Run ID: <unique-run-id>
Input records: 24
Valid records: 20
Rejected records: 4
Published records: 20
Reconciliation status: passed

Pipeline completed successfully!
```

## 9. Run Automated Tests

Execute all automated tests:

```bash
python -m pytest -v
```

The project currently includes **40 automated tests** covering:

- Data generation
- Data ingestion
- Data validation
- Privacy transformations
- Data minimization
- Security validation
- Database publishing
- Reconciliation
- Audit logging
- Pipeline integration
- Failure and retry scenarios
- Data quality and edge cases

**Latest test result: 40 passed.**

Test execution evidence is available in `reports/test_results.txt`.

## 10. Sample Data and Execution Evidence

The `samples/` directory contains synthetic input data and actual pipeline output for demonstration and evaluation.

| File | Description |
|---|---|
| `samples/sample_input.csv` | Synthetic customer input dataset |
| `samples/expected_labels.csv` | Expected validation labels |
| `samples/sample_analytical_output.csv` | Minimized and tokenized analytical output |
| `samples/sample_reconciliation.json` | Pipeline reconciliation results |

### Sample Execution Results

| Metric | Result |
|---|---:|
| Total input records | 24 |
| Valid records | 20 |
| Rejected records | 4 |
| Published records | 20 |
| Reconciliation | Passed |

The expected labels are maintained separately from the input dataset to support validation testing.

The latest successful pipeline execution is documented in `samples/sample_reconciliation.json`.

It includes record counts, reconciliation results, token uniqueness, income totals, and the execution Run ID.

The reconciliation report verifies:

- Input records equal valid records plus rejected records.
- Valid records equal published records.
- Published customer tokens are unique.
- Validated and published income totals match.
- Published records match the validated analytical records at record level.

## 11. Idempotency, Retry, Restart and Backfill

### Idempotency

The pipeline uses staging-based SQLite publishing to avoid duplicate analytical records during repeated publishing operations.

- Data is loaded into a staging table before replacing the target table.
- Duplicate customer tokens are rejected before publishing.
- Repeated publishing of the same dataset produces the expected target record count.
- Automated tests verify repeated publishing and duplicate-token handling.

**Current limitation:** Idempotency is verified at the database publishing stage. Full pipeline-level checkpoint-based idempotency is not implemented.

### Retry Behavior

The pipeline records execution status, errors, and stage-level audit information using a unique Run ID.

If a pipeline stage fails:

1. The failure is recorded in the audit log.
2. Error details are available for investigation.
3. The operator can resolve the issue and execute the pipeline again.
4. The new execution receives a unique Run ID.

Failure and retry scenarios are covered by integration tests.

### Restart Behavior

The current implementation restarts pipeline execution from the beginning.

It does not support automatic recovery from the last successfully completed stage or checkpoint-based continuation.

### Backfill Behavior

Historical data reprocessing is not currently implemented as a dedicated backfill workflow.

A future enhancement could introduce configurable source-file paths, date-range selection, and historical run tracking.

### Reliability Capabilities

| Capability | Implementation |
|---|---|
| Repeated database publishing | Supported and tested |
| Duplicate token prevention | Supported and tested |
| Failure logging | Implemented |
| Retry through a new execution | Tested |
| Automatic checkpoint recovery | Not implemented |
| Dedicated backfill workflow | Future enhancement |

## 12. Performance Benchmark

The pipeline was benchmarked using 100,000 synthetic customer records.

| Metric | Result |
|---|---:|
| Records processed | 100,000 |
| Total execution time | 13.15 seconds |
| Peak Python-tracked memory | 89.27 MB |
| Throughput | 7,603.74 records/second |

The benchmark includes an optimization using pre-generated Faker value pools to reduce repeated data-generation overhead.

Results are from a local benchmark and may vary depending on hardware and system conditions. Memory represents Python-tracked memory, not total process memory.

## 13. Security Considerations

- Sensitive customer fields are removed from the analytical dataset.
- HMAC-SHA256 tokenization protects customer identifiers through pseudonymization.
- Tokenization secrets are supplied through environment variables.
- Invalid records are separated into quarantine.
- Analytical data is checked before publishing.
- Audit logs capture pipeline execution details.
- Data reconciliation verifies source and target record counts.

**Important:** HMAC-SHA256 tokenization is pseudonymization, not encryption or guaranteed anonymization. The security of tokenized data also depends on protecting the secret key.

Annual income is retained for analytical purposes in the current implementation. It may still be sensitive and should be protected through appropriate access controls.

## 14. Design Decisions and Assumptions

The project uses a modular Python architecture, Pandas for tabular processing, SQLite for local analytical publishing, and HMAC-SHA256 for deterministic pseudonymous customer identifiers.

The current solution processes a single customer entity. Multi-entity referential integrity, streaming, and late-arriving event processing are outside the current scope.

The current implementation does not include event-based processing for late-arriving or out-of-order data. Invalid foreign-key reference checks are not applicable because the sample dataset contains only one customer entity and no related entities.

For detailed technology choices and trade-offs, see [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md).

For field definitions and validation rules, see [reports/data_dictionary.md](reports/data_dictionary.md).

## 15. Future Enhancements

- Interactive pipeline monitoring dashboard
- Cloud storage integration
- Distributed processing for larger datasets
- Advanced monitoring and alerting
- Checkpoint-based recovery
- Historical data backfill support
- Multi-entity referential integrity validation
- Historical analytical dataset versioning

## 16. Known Limitations

- **Recovery:** The pipeline supports retry by executing the complete pipeline again after a failure. It does not currently support checkpoint-based restart from the failed stage.
- **Backfill:** A dedicated historical backfill mechanism is not implemented.
- **Late-arriving data:** Event ordering and late-arriving data handling are outside the current scope because the sample project processes customer records rather than an event stream.
- **Referential integrity:** The current dataset contains a single customer entity and does not define foreign-key relationships. Referential integrity checks are therefore not applicable to this implementation.
- **History:** Publishing replaces the analytical snapshot. Historical versions of published datasets are not maintained.
- **Deployment:** The solution currently runs locally using Python, Pandas, and SQLite. Cloud deployment is a possible future enhancement.

## 17. Author

**Vaddevolu HimaBindu**