# Design Decisions and Trade-offs

## 1. Architecture

**Decision:** Use a modular three-tier architecture.

- Presentation Tier: Command-line execution through `main.py`.
- Application Tier: Independent modules for ingestion, profiling, validation, masking, minimization, security, auditing, and publishing.
- Data Tier: CSV files, SQLite database, JSON reports, and audit logs.

**Reason:** Separating responsibilities improves maintainability, testing, and future extensibility.

## 2. Technology Choices

| Technology | Purpose | Reason |
|---|---|---|
| Python | Pipeline implementation | Readable and extensible |
| Pandas | Data processing | Efficient tabular transformations |
| Faker | Synthetic data generation | Reproducible test datasets |
| SQLite | Analytical publishing | Lightweight local database |
| JSON | Configuration and reports | Simple and readable |
| Pytest | Automated testing | Repeatable test execution |

## 3. Privacy Strategy

**Decision:** Use HMAC-SHA256 tokenization for customer identifiers.

**Reason:** Provides deterministic pseudonymous identifiers when the same secret key is used.

Sensitive fields are masked or removed based on configurable privacy rules.

**Trade-off:** Tokenization is pseudonymization, not anonymization. The secret key must be protected.

## 4. Data Quality Strategy

**Decision:** Validate records before privacy transformation and publishing.

Validation covers:
- Required fields
- Duplicate customer identifiers
- Email format
- Phone format
- Age boundaries
- Annual income
- Registration dates

Invalid records are separated into a rejected-record output with traceability information.

## 5. Publishing Strategy

**Decision:** Use a SQLite staging table before replacing the analytical target table.

**Reason:** Allows validation of staged record counts before publishing the new snapshot.

**Trade-off:** The current implementation maintains a latest analytical snapshot rather than historical analytical versions.

## 6. Performance Optimization

**Decision:** Reuse pre-generated Faker value pools when generating large datasets.

**Reason:** Reduces repeated Faker object generation overhead.

**Measured result:** The 100,000-record benchmark improved from approximately 93.69 seconds to 13.15 seconds in the recorded local benchmark.

Results depend on the execution environment.

## 7. Scope and Limitations

- The current pipeline processes a single customer entity.
- Foreign-key relationship validation is not applicable to the current single-entity dataset.
- Streaming and late-arriving event processing are not implemented.
- Automatic checkpoint recovery is not implemented.
- Dedicated historical backfill is not implemented.
- Analytical publishing replaces the current snapshot.

## 8. Future Improvements

- Add checkpoint-based recovery.
- Support historical backfills.
- Add multi-entity referential integrity validation.
- Introduce a monitoring dashboard.
- Support cloud storage and distributed processing.
