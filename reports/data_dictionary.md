
# Data Dictionary

## Input Dataset: customers.csv

| Column | Description | Data Type | Sensitive |
|---|---|---|---|
| customer_id | Unique customer identifier | String | Yes |
| full_name | Customer full name | String | Yes |
| email | Customer email address | String | Yes |
| phone | Customer phone number | String | Yes |
| age | Customer age | Integer | No |
| city | Customer city | String | No |
| annual_income | Customer annual income | Numeric | Yes |
| registration_date | Customer registration date | Date | No |
| source_row_number | Original source row number | Integer | No |

## Published Dataset: analytical_customers

| Column | Description |
|---|---|
| customer_token | HMAC-SHA256 customer token |
| age | Customer age |
| city | Customer city |
| annual_income | Customer annual income |
| registration_date | Customer registration date |

## Privacy Notes

- Customer IDs are tokenized using HMAC-SHA256.
- Names, emails, and phone numbers are masked.
- Original sensitive columns are removed before publishing.
- Only minimized analytical data is published to SQLite.
