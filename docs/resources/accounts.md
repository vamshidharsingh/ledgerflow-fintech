# Accounts

Currency-specific wallets. Balances change only through transfers or simulated deposits.

| Field | Type | Constraint |
| --- | --- | --- |
| `customer_id` | string | Reference to `customers` |
| `name` | string | Required |
| `currency` | string | USD, EUR, INR |
| `balance_cents` | integer | Required |
| `status` | string | active, frozen |

Read endpoint: `GET /api/resources/accounts`. A local operator bearer token is required.
This resource is read-only through the generic HTTP API. Use the documented business workflows so derived state remains consistent.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `[]`.
Fixture file: `fixtures/accounts.json`. Repository exact-match helper: `find_by_customer_id`.
Test module: `tests/test_accounts.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
