# Data Dictionary

## 1. Input Dataset: `customers.csv`

**Entity:** Customer

**Grain:** One row represents one customer source record.

| Column | Description | Data Type | Sensitive |
|---|---|---|---|
| customer_id | Customer business identifier | String | Yes |
| full_name | Customer full name | String | Yes |
| email | Customer email address | String | Yes |
| phone | Customer phone number | String | Yes |
| age | Customer age in years | Integer | No |
| city | Customer city | String | No |
| annual_income | Customer annual income | Numeric | Yes |
| registration_date | Customer registration date | Date | No |
| source_row_number | Original source row number for traceability | Integer | No |

## 2. Published Dataset: `analytical_customers`

**Storage:** SQLite

**Grain:** One row represents one validated customer.

| Column | Description | Data Type | Sensitive |
|---|---|---|---|
| customer_token | Deterministic HMAC-SHA256 customer token | String | Pseudonymous |
| age | Customer age in years | Integer | No |
| city | Customer city | String | No |
| annual_income | Customer annual income retained for analytics | Numeric | Yes - retained with access restrictions |
| registration_date | Customer registration date | Date | No |

**Privacy Note:** Annual income remains potentially sensitive personal information even after direct identifiers are removed. It is retained for analytical purposes and must be protected through appropriate access controls. Removing direct identifiers does not guarantee complete anonymization.

## 3. Validation Rules

| Field | Validation Rule |
|---|---|
| customer_id | Required and unique |
| full_name | Required |
| email | Required and valid email format |
| phone | Required and 10-digit format |
| age | Required integer between 18 and 100 |
| city | Required |
| annual_income | Required positive numeric value |
| registration_date | Required and parseable as a date |

Invalid records are separated from valid records and written to the rejected-record output with rejection reasons and source traceability.

## 4. Privacy Transformation Rules

- `customer_id` is tokenized using HMAC-SHA256.
- `full_name`, `email`, and `phone` are masked according to configurable privacy rules.
- Original sensitive columns are removed before analytical publishing.
- The HMAC secret is supplied through an environment variable and must not be committed to source control.
- HMAC tokenization provides pseudonymization, not anonymization.
- `annual_income` is retained for analytics and remains potentially sensitive.

## 5. Published Data Minimization

Only the following columns are published:

- `customer_token`
- `age`
- `city`
- `annual_income`
- `registration_date`

The published dataset is stored in the SQLite analytical database.

Although direct identifiers are removed, retained analytical attributes may still carry privacy risks. Access to the published dataset should therefore be restricted according to its intended use.

## 6. Audit and Traceability

The pipeline records:

- Unique pipeline Run ID
- Execution timestamps
- Processing stage and status
- Input and output record counts
- Rejected record counts
- Failure details and execution duration

Audit entries are stored in `logs/audit.jsonl`.

## 7. Assumptions and Scope

- The current implementation processes a single customer entity.
- Customer identifiers are expected to be unique.
- The published analytical table represents the latest snapshot.
- Historical analytical versions and multi-entity relationships are outside the current implementation scope.
- Synthetic data is used for development and testing.