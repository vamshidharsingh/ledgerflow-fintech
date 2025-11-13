# Expenses

Manual spend annotations separate from the banking ledger.

| Field | Type | Constraint |
| --- | --- | --- |
| `account_id` | string | Reference to `accounts` |
| `category_id` | string | Reference to `categories` |
| `amount_cents` | integer | Required |
| `description` | string | Required |
| `date` | string | date |

Read endpoint: `GET /api/resources/expenses`. A local operator bearer token is required.
Create, update and delete are supported by the operator resource API. PUT is a full replacement and requires `_version`; deletes require a version query parameter.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `[]`.
Fixture file: `fixtures/expenses.json`. Repository exact-match helper: `find_by_account_id`.
Test module: `tests/test_expenses.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
